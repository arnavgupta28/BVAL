"""BVAL pricing engine.

Pure, deterministic functions with no Apify or network dependency. Every number comes from
`config/rates.json`, which cites a source (or `assumption`) for each value. The LLM never sets a price.

Pipeline (see bval_research.md, section 3):
    views basis -> raw base -> engagement adjustment -> tier clamp -> (India factor) -> package discount
    -> add-ons as % of content base -> fair / ask / floor / walk-away -> verdict -> red flags -> reduced scope
"""

from __future__ import annotations

import json
import math
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RATES_PATH = Path(__file__).parent / 'config' / 'rates.json'

DISCLAIMER = (
    'Benchmark-based estimate from public 2026 industry sources, not financial or legal advice. '
    'Rates vary 2-10x across sources; use this as a negotiation anchor.'
)

PERPETUAL_DAYS = 100_000  # sentinel for "perpetual" usage

# Order in which scope is traded away when building the reduced-scope counter option.
REDUCTION_ORDER = [
    'rush',
    'revisions',
    'raw_footage',
    'cross_post',
    'paid_usage',
    'exclusivity',
    'whitelisting',
    'link_in_bio',
    'story_link_sticker',
    'pinned_comment_link',
    'organic_usage',
]


def load_rates(path: Path = RATES_PATH) -> dict[str, Any]:
    return json.loads(path.read_text())


class PricingError(ValueError):
    """Raised for inputs the engine cannot price (unknown deliverable, no metrics on YouTube, ...)."""


# --------------------------------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------------------------------


@dataclass
class Metrics:
    """Creator performance metrics, already normalised by the feeders (or supplied manually)."""

    platform: str
    audience: int | None  # followers (IG, TikTok) or subscribers (YouTube)
    median_views: dict[str, float | None] = field(default_factory=dict)  # keyed by anchor deliverable
    engagement_rate: dict[str, float | None] = field(default_factory=dict)  # keyed by anchor deliverable
    sample_size: dict[str, int] = field(default_factory=dict)
    views_field: str | None = None  # IG: which play-count field was used
    volatility: float | None = None  # TikTok p75/p25 of plays
    age_fallback: bool = False  # YouTube long-form fell back to the 7-day window
    likes_hidden: bool = False
    source: str = 'scraped'  # scraped | manual


@dataclass
class Terms:
    """The brand's requested deal terms."""

    deliverables: list[dict[str, Any]]  # [{"type": "instagram_reel", "qty": 1}]
    niche: str = 'lifestyle'
    organic_usage_days: int = 0
    paid_usage_days: int = 0
    whitelisting_days: int = 0
    exclusivity_days: int = 0
    exclusivity_scope: str = 'category'  # category | full
    perpetual_rights: bool = False
    rush_hours: int = 0  # 0 = standard turnaround
    revision_rounds: int = 1
    raw_footage: bool = False
    link_in_bio_days: int = 0
    story_link_sticker: bool = False
    pinned_comment_link: bool = False
    cross_post_platforms: int = 0
    payment_terms_days: int = 30
    deposit_pct: int = 50
    ai_training_clause: bool = False
    ad_spend_usd: float | None = None
    offer_amount: float | None = None
    offer_currency: str = 'USD'
    gifted_only: bool = False
    market: str = 'global'  # global | india
    output_currency: str = 'USD'  # USD | INR


# --------------------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------------------


def tier_for(audience: int | None, rates: dict) -> str:
    if not audience:
        return 'nano'
    for name, (lo, hi) in rates['tier_bounds'].items():
        if audience >= lo and (hi is None or audience < hi):
            return name
    return 'nano'  # below 1K


def bucket(table: dict[str, float], days: int) -> float:
    """Smallest bucket >= requested days; > max numeric bucket or perpetual -> 'perpetual' (or max)."""
    if days <= 0:
        return 0.0
    numeric = sorted(int(k) for k in table if k.isdigit())
    for b in numeric:
        if days <= b:
            return float(table[str(b)])
    if 'perpetual' in table:
        return float(table['perpetual'])
    # No perpetual key (exclusivity): scale the top bucket linearly.
    top = numeric[-1]
    return float(table[str(top)]) * days / top


def whitelisting_pct(days: int, rates: dict) -> float:
    t = rates['addons']['whitelisting_pct']
    if days <= 0:
        return 0.0
    if days <= 30:
        return float(t['30'])
    if days <= 60:
        return float(t['60'])
    if days <= 90:
        return float(t['90'])
    extra_blocks = math.ceil((days - 90) / 30)
    return float(t['90']) + extra_blocks * float(t['each_extra_30'])


def engagement_adjustment(er: float | None, low: float, high: float, curve: dict) -> float:
    """Piecewise-linear: 0 -> at_zero, low -> at_low, high -> at_high, 2*high -> at_2x_high, capped."""
    if er is None:
        return float(curve['hidden_likes_adj'])
    pts = [(0.0, curve['at_zero']), (low, curve['at_low']), (high, curve['at_high']), (2 * high, curve['at_2x_high'])]
    if er >= pts[-1][0]:
        return float(curve['cap'])
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= er <= x1:
            return y0 + (y1 - y0) * (er - x0) / (x1 - x0)
    return float(curve['at_zero'])


def er_band(audience: int | None, bands: list[dict]) -> tuple[float, float]:
    a = audience or 0
    for b in bands:
        lo, hi = b['audience']
        if a >= lo and (hi is None or a < hi):
            return b['low'], b['high']
    return bands[-1]['low'], bands[-1]['high']


def sources_for(path: str, rates: dict) -> list[str]:
    """Most specific `sources` entry covering a config path."""
    src = rates['sources']
    parts = path.split('.')
    while parts:
        key = '.'.join(parts)
        if key in src:
            return src[key]
        parts.pop()
    return ['assumption']


def round_to(value: float, step: int) -> float:
    return float(round(value / step) * step)


# --------------------------------------------------------------------------------------------------
# Core pricing
# --------------------------------------------------------------------------------------------------


def _deliverable_def(platform_cfg: dict, dtype: str) -> tuple[dict, str, dict]:
    """Return (deliverable cfg, anchor name, anchor cfg)."""
    dels = platform_cfg['deliverables']
    if dtype not in dels:
        raise PricingError(f'Deliverable "{dtype}" is not offered on this platform. Options: {", ".join(dels)}.')
    d = dels[dtype]
    anchor = d.get('priced_from', dtype)
    return d, anchor, dels[anchor]


def _engagement_cfg(platform: str, anchor: str, platform_cfg: dict) -> dict:
    eng = platform_cfg['engagement']
    if platform == 'youtube':
        return eng['shorts'] if anchor == 'youtube_short' else eng['long_form']
    return eng


def price_unit(dtype: str, metrics: Metrics, terms: Terms, rates: dict, tier: str) -> dict:
    """Price one unit of a deliverable. Returns a dict with the unit price and how it was derived."""
    platform_cfg = rates['platforms'][metrics.platform]
    d, anchor, anchor_cfg = _deliverable_def(platform_cfg, dtype)
    ratio = float(d.get('ratio', 1.0))

    niche_mults = rates['niche_multipliers']
    niche = terms.niche if terms.niche in niche_mults else 'other'
    niche_mult = float(niche_mults[niche])
    if terms.market == 'india' and niche in niche_mults.get('india_overrides', {}):
        niche_mult = float(niche_mults['india_overrides'][niche])

    views = metrics.median_views.get(anchor)
    method = 'views'
    if views:
        raw = views / 1000 * anchor_cfg['cpm_usd'] * ratio * niche_mult
    else:
        per_1k = platform_cfg.get('follower_fallback_usd_per_1k')
        if per_1k is None or not metrics.audience:
            raise PricingError(
                f'No usable view data for {anchor} and no follower fallback on {metrics.platform}. '
                'Supply manualMetrics (median views) to price this deliverable.'
            )
        raw = metrics.audience / 1000 * per_1k * ratio * niche_mult
        method = 'follower_fallback'

    eng_cfg = _engagement_cfg(metrics.platform, anchor, platform_cfg)
    if eng_cfg.get('enabled') and method == 'views':
        low, high = er_band(metrics.audience, eng_cfg['bands'])
        er = metrics.engagement_rate.get(anchor)
        er_adj = engagement_adjustment(er, low, high, rates['engagement_curve'])
    else:
        low = high = er = None
        er_adj = 1.0

    lo_clamp, hi_clamp = anchor_cfg['clamp_usd'][tier]
    lo_clamp, hi_clamp = lo_clamp * ratio, hi_clamp * ratio
    adjusted = raw * er_adj
    unit = min(max(adjusted, lo_clamp), hi_clamp)
    clamped = not math.isclose(unit, adjusted)

    india_factor = 1.0
    if terms.market == 'india':
        india_factor = float(rates['currency']['india_market_factor_by_tier'][tier])
        unit *= india_factor

    return {
        'type': dtype,
        'anchor': anchor,
        'method': method,
        'medianViews': views,
        'cpmUsd': anchor_cfg['cpm_usd'],
        'ratio': ratio,
        'nicheMultiplier': niche_mult,
        'engagementRate': er,
        'engagementBand': [low, high] if low is not None else None,
        'erAdjustment': round(er_adj, 4),
        'raw': raw,
        'clampUsd': [lo_clamp, hi_clamp],
        'clamped': clamped,
        'indiaFactor': india_factor,
        'unitUsd': unit,
    }


def package_discount(total_qty: int, rates: dict) -> float:
    t = rates['package_discounts_pct']
    if total_qty >= 3:
        pct = t['3_plus']
    elif total_qty == 2:
        pct = t['2']
    else:
        pct = 0
    return min(pct, t['max']) / 100


def _na_set(platform: str, rates: dict) -> set[str]:
    return set(rates['platforms'][platform].get('not_applicable', []))


def compute_addons(content_base: float, terms: Terms, platform: str, tier: str, rates: dict) -> tuple[list[dict], list[str]]:
    """Return (line items, warnings) for every add-on, priced as % of content base."""
    a = rates['addons']
    pcfg = rates['platforms'][platform]
    padd = pcfg['platform_addons']
    na = _na_set(platform, rates)
    tier_mult = float(a['usage_tier_multiplier'][tier])
    # Fixed USD minimums come from US sources; scale them like every other price in India-market mode.
    min_scale = float(rates['currency']['india_market_factor_by_tier'][tier]) if terms.market == 'india' else 1.0
    items: list[dict] = []
    warnings: list[str] = []

    def add(key: str, label: str, pct: float | None, amount: float, src_path: str, days: int | None = None) -> None:
        srcs = sources_for(src_path, rates)
        items.append({
            'key': key,
            'item': label,
            'pctOfBase': round(pct, 2) if pct is not None else None,
            'amountUsd': amount,
            'durationDays': days,
            'sources': srcs,
            'isAssumption': srcs == ['assumption'],
        })

    organic_days = PERPETUAL_DAYS if terms.perpetual_rights else terms.organic_usage_days
    paid_days = PERPETUAL_DAYS if (terms.perpetual_rights and terms.paid_usage_days) else terms.paid_usage_days

    # Organic usage
    if organic_days > 0:
        pct = bucket(a['organic_usage_pct'], organic_days) * tier_mult
        label = 'Organic usage rights, perpetual' if organic_days >= PERPETUAL_DAYS else f'Organic usage rights, {organic_days} days'
        add('organic_usage', label, pct, content_base * pct / 100, 'addons.organic_usage_pct', None if organic_days >= PERPETUAL_DAYS else organic_days)

    # Whitelisting / Partnership Ads / Spark Ads
    wl_days = terms.whitelisting_days
    if wl_days > 0:
        if 'whitelisting' in na or not padd.get('whitelisting_name'):
            warnings.append('Handle whitelisting is not offered on YouTube; price brand ads as paid usage instead.')
            wl_days = 0
        else:
            name = {'meta_partnership_ads': 'Meta Partnership Ads', 'tiktok_spark_ads': 'TikTok Spark Ads'}[padd['whitelisting_name']]
            pct = whitelisting_pct(wl_days, rates) * tier_mult * float(padd['whitelisting_factor'])
            amount = content_base * pct / 100
            amount = max(amount, a['whitelisting_min_usd_per_30d'] * min_scale * math.ceil(wl_days / 30))
            if terms.ad_spend_usd:
                amount = max(amount, terms.ad_spend_usd * a['whitelisting_ad_spend_pct'] / 100)
            add('whitelisting', f'{name} (whitelisting), {wl_days} days', pct, amount, 'addons.whitelisting_pct', wl_days)

    # Paid usage, charged only beyond the whitelisting window
    if paid_days > 0:
        base_pct = bucket(a['paid_usage_pct'], paid_days) - bucket(a['paid_usage_pct'], wl_days)
        pct = max(base_pct, 0.0) * tier_mult
        if pct > 0:
            label = 'Paid usage rights (brand ads), perpetual' if paid_days >= PERPETUAL_DAYS else f'Paid usage rights (brand ads), {paid_days} days'
            if wl_days:
                label += f', beyond the {wl_days}-day whitelisting window'
            add('paid_usage', label, pct, content_base * pct / 100, 'addons.paid_usage_pct', None if paid_days >= PERPETUAL_DAYS else paid_days)

    # Exclusivity
    if terms.exclusivity_days > 0:
        pct = bucket(a['exclusivity_category_pct'], terms.exclusivity_days)
        if pct > 0:
            crowded = terms.niche in a['crowded_categories']
            pct *= a['exclusivity_crowding_factor']['crowded' if crowded else 'standard']
            if terms.exclusivity_scope == 'full':
                pct *= a['exclusivity_full_factor']
            amount = max(content_base * pct / 100, a['exclusivity_min_usd'] * min_scale, content_base * a['exclusivity_min_pct_of_base'] / 100)
            scope = 'Full exclusivity (no other brands)' if terms.exclusivity_scope == 'full' else f'Category exclusivity ({terms.niche})'
            add('exclusivity', f'{scope}, {terms.exclusivity_days} days', pct, amount, 'addons.exclusivity_category_pct', terms.exclusivity_days)

    # Rush
    if 0 < terms.rush_hours < 72:
        pct = a['rush_pct']['under_24h'] if terms.rush_hours < 24 else a['rush_pct']['under_72h']
        add('rush', f'Rush delivery (under {terms.rush_hours}h)', pct, content_base * pct / 100, 'addons.rush_pct')

    # Revisions
    rev = a['revisions']
    extra = max(0, terms.revision_rounds - rev['included_rounds'])
    if extra:
        each = max(content_base * rev['extra_round_pct'] / 100, rev['extra_round_min_usd'] * min_scale)
        add('revisions', f'Extra revision rounds x{extra} ({rev["included_rounds"]} included)', rev['extra_round_pct'] * extra, each * extra, 'addons.revisions')

    # Raw footage
    if terms.raw_footage:
        pct = a['raw_footage_pct']
        add('raw_footage', 'Raw footage / unedited files', pct, content_base * pct / 100, 'addons.raw_footage_pct')

    # Cross-posting
    if terms.cross_post_platforms > 0:
        pct = a['cross_post_pct_per_platform'] * terms.cross_post_platforms
        add('cross_post', f'Cross-post to {terms.cross_post_platforms} other platform(s)', pct, content_base * pct / 100, 'addons.cross_post_pct_per_platform')

    # Platform-specific placements
    if terms.link_in_bio_days > 0:
        if 'link_in_bio' in na or 'link_in_bio_7d_pct' not in padd:
            warnings.append('Link in bio does not apply on YouTube; use the description or pinned-comment link.')
        else:
            pct = padd['link_in_bio_7d_pct'] * math.ceil(terms.link_in_bio_days / 7)
            add('link_in_bio', f'Link in bio, {terms.link_in_bio_days} days', pct, content_base * pct / 100, f'platforms.{platform}.platform_addons.link_in_bio_7d_pct', terms.link_in_bio_days)

    if terms.story_link_sticker:
        if 'story_link_sticker_pct' not in padd:
            warnings.append('Story link stickers only apply on Instagram.')
        else:
            pct = padd['story_link_sticker_pct']
            add('story_link_sticker', 'Story link sticker', pct, content_base * pct / 100, f'platforms.{platform}.platform_addons.story_link_sticker_pct')

    if platform == 'youtube':
        add('description_link', 'Link in video description', 0.0, 0.0, 'platforms.youtube.platform_addons')
    if terms.pinned_comment_link:
        if 'pinned_comment_link_pct' not in padd:
            warnings.append('Pinned-comment links only apply on YouTube.')
        else:
            pct = padd['pinned_comment_link_pct']
            add('pinned_comment_link', 'Pinned-comment link', pct, content_base * pct / 100, 'platforms.youtube.platform_addons')

    return items, warnings


def _evaluate_scope(metrics: Metrics, terms: Terms, rates: dict) -> dict:
    """Price a full scope: deliverables + add-ons -> fair value (USD)."""
    tier = tier_for(metrics.audience, rates)
    units = []
    total_qty = 0
    gross = 0.0
    for d in terms.deliverables:
        qty = int(d.get('qty', 1))
        if qty <= 0:
            continue
        u = price_unit(d['type'], metrics, terms, rates, tier)
        u['qty'] = qty
        u['subtotalUsd'] = u['unitUsd'] * qty
        units.append(u)
        total_qty += qty
        gross += u['subtotalUsd']
    if not units:
        raise PricingError('At least one deliverable with qty >= 1 is required.')
    disc = package_discount(total_qty, rates)
    content_base = gross * (1 - disc)
    addons, warnings = compute_addons(content_base, terms, metrics.platform, tier, rates)
    fair = content_base + sum(i['amountUsd'] for i in addons)
    return {
        'tier': tier,
        'units': units,
        'grossUsd': gross,
        'packageDiscountPct': disc * 100,
        'contentBaseUsd': content_base,
        'addons': addons,
        'warnings': warnings,
        'fairUsd': fair,
    }


def min_scope_terms(terms: Terms, rates: dict) -> Terms:
    ms = rates['negotiation']['min_scope']
    t = deepcopy(terms)
    t.organic_usage_days = ms['organic_usage_days']
    t.paid_usage_days = ms['paid_usage_days']
    t.whitelisting_days = ms['whitelisting_days']
    t.exclusivity_days = min(terms.exclusivity_days, ms['exclusivity_days'])
    t.exclusivity_scope = 'category'
    t.perpetual_rights = False
    t.rush_hours = 0
    t.revision_rounds = min(terms.revision_rounds, rates['addons']['revisions']['included_rounds'])
    t.raw_footage = False
    t.cross_post_platforms = 0
    t.link_in_bio_days = 0
    t.story_link_sticker = False
    t.pinned_comment_link = False
    t.ad_spend_usd = None
    return t


def _drop(terms: Terms, key: str, rates: dict) -> Terms:
    """Remove (or shrink to minimum) one tradeable term."""
    t = deepcopy(terms)
    ms = rates['negotiation']['min_scope']
    if key == 'rush':
        t.rush_hours = 0
    elif key == 'revisions':
        t.revision_rounds = min(t.revision_rounds, rates['addons']['revisions']['included_rounds'])
    elif key == 'raw_footage':
        t.raw_footage = False
    elif key == 'cross_post':
        t.cross_post_platforms = 0
    elif key == 'paid_usage':
        t.paid_usage_days = 0
        if t.perpetual_rights:
            t.perpetual_rights = False
    elif key == 'exclusivity':
        t.exclusivity_days = min(t.exclusivity_days, ms['exclusivity_days'])
        t.exclusivity_scope = 'category'
    elif key == 'whitelisting':
        t.whitelisting_days = 0
        t.ad_spend_usd = None
    elif key == 'link_in_bio':
        t.link_in_bio_days = 0
    elif key == 'story_link_sticker':
        t.story_link_sticker = False
    elif key == 'pinned_comment_link':
        t.pinned_comment_link = False
    elif key == 'organic_usage':
        t.perpetual_rights = False
        t.organic_usage_days = min(t.organic_usage_days, ms['organic_usage_days']) if t.organic_usage_days else 0
    return t


def reduced_scope(metrics: Metrics, terms: Terms, rates: dict, offer_usd: float | None, full_fair: float) -> dict | None:
    """Trade scope away (in REDUCTION_ORDER) until the price is within 10% of the brand's budget.

    Never goes below the minimum scope. Returns None if nothing can be dropped.
    """
    target = (offer_usd or 0) * 1.10
    current = terms
    dropped: list[str] = []
    last = None
    for key in REDUCTION_ORDER:
        candidate = _drop(current, key, rates)
        if candidate == current:
            continue
        current = candidate
        dropped.append(key)
        last = _evaluate_scope(metrics, current, rates)
        if offer_usd is not None and last['fairUsd'] <= target:
            break
    if last is None or math.isclose(last['fairUsd'], full_fair):
        return None
    return {'droppedOrReduced': dropped, 'terms': current, 'scope': last, 'priceUsd': last['fairUsd']}


def verdict_for(offer: float | None, pts: dict) -> str:
    if offer is None:
        return 'NO_OFFER'
    if offer >= pts['ask']:
        return 'ACCEPT_STRONG'
    if offer >= pts['fair']:
        return 'ACCEPT'
    if offer >= pts['floor']:
        return 'COUNTER_LIGHT'
    if offer >= pts['walkAway']:
        return 'COUNTER_TRADE_SCOPE'
    return 'DECLINE_OR_REDUCE_SCOPE'


VERDICT_TEXT = {
    'ACCEPT_STRONG': 'Offer is at or above your ask. Accept and confirm the terms in writing.',
    'ACCEPT': 'Offer is fair. Accept and restate the scope so nothing extra creeps in.',
    'COUNTER_LIGHT': 'Offer is slightly below fair value. Counter at your ask and settle at fair or above.',
    'COUNTER_TRADE_SCOPE': 'Offer is well below fair value. Offer full scope at your ask, or a reduced scope at their budget.',
    'DECLINE_OR_REDUCE_SCOPE': 'Offer is below your walk-away point. Decline warmly, or offer only the minimum scope.',
    'NO_OFFER': 'No offer supplied. Use the ask as your quote.',
}


def red_flags(terms: Terms, metrics: Metrics, pts: dict, offer_usd: float | None, scope: dict, without_wl_fair: float | None, rates: dict) -> list[dict]:
    lim = rates['negotiation']['red_flag_limits']
    na = _na_set(metrics.platform, rates)
    flags: list[dict] = []
    amounts = {i['key']: i['amountUsd'] for i in scope['addons']}

    def flag(code: str, msg: str) -> None:
        flags.append({'code': code, 'message': msg})

    if terms.perpetual_rights or terms.organic_usage_days > 365 or terms.paid_usage_days > 365:
        flag('PERPETUAL_RIGHTS', 'Perpetual or 12+ month usage requested. Counter with a 12-month licence plus renewals.')
    if terms.whitelisting_days and without_wl_fair is not None and offer_usd is not None and offer_usd < without_wl_fair:
        flag('UNPRICED_WHITELISTING', 'Ads through your handle are requested, but the offer does not even cover the deal without them.')
    short_form = metrics.platform in ('instagram', 'tiktok') or any(d['type'] == 'youtube_short' for d in terms.deliverables)
    if short_form and terms.paid_usage_days > lim['paid_usage_days_overbuy']:
        flag('USAGE_OVERBUY', f'Paid usage over {lim["paid_usage_days_overbuy"]} days on short-form content, which peaks in 4-6 weeks.')
    if terms.exclusivity_days > lim['exclusivity_days_unpaid_max'] or terms.exclusivity_scope == 'full' and terms.exclusivity_days > 0:
        extra = amounts.get('exclusivity')
        msg = f'Exclusivity beyond {lim["exclusivity_days_unpaid_max"]} days'
        msg += f' is worth +${extra:,.0f} on its own.' if extra else '.'
        flag('LONG_EXCLUSIVITY', msg)
    if (terms.gifted_only or offer_usd == 0) and (terms.organic_usage_days or terms.paid_usage_days or terms.exclusivity_days):
        flag('GIFTED_FOR_RIGHTS', 'Product-only or unpaid offer that still asks for usage or exclusivity. Never grant rights for gifted product.')
    if terms.ai_training_clause:
        flag('AI_LIKENESS', 'AI training or likeness clause present. Strike it or price it separately.')
    if terms.payment_terms_days > lim['payment_terms_days_max'] or terms.deposit_pct < lim['deposit_pct_min']:
        flag('SLOW_PAY_NO_DEPOSIT', f'Payment terms of Net {terms.payment_terms_days} with a {terms.deposit_pct}% deposit. Ask for 50% upfront and Net 30.')
    if 0 < terms.rush_hours < 72 and offer_usd is not None and offer_usd < pts['fair']:
        flag('RUSH_UNPAID', 'Rush turnaround requested without paying for it (+35-50% is standard).')
    if terms.revision_rounds > lim['included_revisions_max']:
        flag('EXCESS_REVISIONS', f'{terms.revision_rounds} revision rounds requested; 1 is standard.')
    if terms.raw_footage and offer_usd is not None and offer_usd < pts['fair']:
        flag('FREE_RAW_FOOTAGE', 'Raw footage requested but not paid for (+20-30% is standard).')
    total_qty = sum(int(d.get('qty', 1)) for d in terms.deliverables)
    if total_qty >= 3 and offer_usd is not None and offer_usd < 0.85 * pts['fair']:
        flag('BUNDLE_SQUEEZE', 'Several deliverables bundled at a price well under the discounted package value.')
    if terms.whitelisting_days and 'whitelisting' in na:
        flag('NA_TERM', 'Whitelisting was requested on a platform that does not support it.')
    return flags


def confidence_for(metrics: Metrics, units: list[dict]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    levels = ['high', 'medium', 'low', 'very_low']
    level = 0
    if any(u['method'] == 'follower_fallback' for u in units):
        return 'very_low', ['No usable view data; priced from follower count.']
    if metrics.source == 'manual':
        reasons.append('Metrics supplied manually, not scraped.')
        level = max(level, 1)
    n = min((metrics.sample_size.get(u['anchor'], 0) for u in units), default=0)
    if metrics.source == 'scraped' and n < 6:
        reasons.append(f'Only {n} usable posts.')
        level = max(level, 2)
    elif metrics.source == 'scraped' and n < 12:
        reasons.append(f'{n} usable posts (12+ preferred).')
        level = max(level, 1)
    if metrics.views_field and metrics.views_field != 'videoPlayCount':
        reasons.append(f'Used fallback views field {metrics.views_field}.')
        level = max(level, 1)
    if metrics.age_fallback:
        reasons.append('Few long-form videos 30+ days old; used videos 7+ days old.')
        level = max(level, 1)
    if any(u['clamped'] for u in units):
        reasons.append('View-based price fell outside the tier band and was clamped.')
        level = max(level, 1)
    if metrics.likes_hidden:
        reasons.append('Likes hidden; engagement adjustment skipped.')
        level = max(level, 1)
    if metrics.volatility and metrics.volatility > 4:
        reasons.append(f'Highly variable views (p75/p25 = {metrics.volatility:.1f}).')
        level = max(level, 1)
    return levels[level], reasons


def evaluate_deal(metrics: Metrics, terms: Terms, rates: dict | None = None) -> dict:
    """Full evaluation: line items, price points, verdict, red flags, reduced-scope option. Amounts in USD."""
    rates = rates or load_rates()
    if metrics.platform not in rates['platforms']:
        raise PricingError(f'Unsupported platform "{metrics.platform}".')

    fx = float(rates['currency']['usd_inr'])
    offer_usd = None
    if terms.offer_amount is not None:
        offer_usd = terms.offer_amount / fx if terms.offer_currency.upper() == 'INR' else float(terms.offer_amount)
    if terms.gifted_only and offer_usd is None:
        offer_usd = 0.0

    scope = _evaluate_scope(metrics, terms, rates)
    fair = scope['fairUsd']
    neg = rates['negotiation']
    min_scope = _evaluate_scope(metrics, min_scope_terms(terms, rates), rates)
    walk_away = min(neg['walk_away_mult_of_min_scope'] * min_scope['fairUsd'], neg['floor_mult'] * fair)
    pts = {'walkAway': walk_away, 'floor': neg['floor_mult'] * fair, 'fair': fair, 'ask': neg['ask_mult'] * fair}

    without_wl = None
    if terms.whitelisting_days:
        t2 = deepcopy(terms)
        t2.whitelisting_days = 0
        without_wl = _evaluate_scope(metrics, t2, rates)['fairUsd']

    verdict = verdict_for(offer_usd, pts)
    flags = red_flags(terms, metrics, pts, offer_usd, scope, without_wl, rates)
    reduced = reduced_scope(metrics, terms, rates, offer_usd, fair) if verdict not in ('ACCEPT', 'ACCEPT_STRONG') else None
    conf, conf_reasons = confidence_for(metrics, scope['units'])

    return {
        'tier': scope['tier'],
        'scope': scope,
        'pricePointsUsd': pts,
        'offerUsd': offer_usd,
        'gapPct': (1 - offer_usd / fair) * 100 if offer_usd is not None and fair else None,
        'verdict': verdict,
        'verdictText': VERDICT_TEXT[verdict],
        'redFlags': flags,
        'reducedScope': reduced,
        'minScopeFairUsd': min_scope['fairUsd'],
        'confidence': conf,
        'confidenceReasons': conf_reasons,
        'warnings': scope['warnings'],
        'ratesVersion': rates['version'],
        'usdInr': fx,
    }
