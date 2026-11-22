"""The numbers BVAL pulled, each with the benchmark it was compared to and the claim it supports.

Built from the main deliverable's pricing trace (pricing.price_unit), so every claim is the arithmetic the engine
actually did, not a separate story. Read top to bottom it explains the base price: audience sets the band,
views x CPM gives the starting price, engagement, niche and market adjust it, the tier range caps it.
"""

from __future__ import annotations

from typing import Any, Callable

from .counter_email import deliverable_label

AUDIENCE_WORD = {'instagram': 'followers', 'tiktok': 'followers', 'youtube': 'subscribers'}


def build_evidence(unit: dict, metrics: Any, info: dict, tier: str, rates: dict, market: dict,
                   niche: str, money: Callable[[float], str]) -> list[dict[str, str]]:
    """unit: the main deliverable's entry from scope['units'] (one price_unit trace)."""
    out: list[dict[str, str]] = []
    label = deliverable_label(unit['type'])
    word = AUDIENCE_WORD.get(metrics.platform, 'followers')
    mf = unit.get('marketFactor') or 1.0

    def add(stat: str, value: str, benchmark: str, claim: str) -> None:
        out.append({'stat': stat, 'value': value, 'benchmark': benchmark, 'claim': claim})

    if metrics.audience:
        lo, hi = rates['tier_bounds'][tier]
        band = f'{lo:,}+' if hi is None else f'{lo:,} to {hi:,}'
        clamp_lo, clamp_hi = unit['clampUsd']
        claim = f'Keeps one {label} between {money(clamp_lo * mf)} and {money(clamp_hi * mf)}.'
        if unit.get('clamped'):
            claim += ' Your views-based price fell outside it, so it was moved to the edge of the range.'
        add('Audience', f'{metrics.audience:,} {word}', f'{tier.title()} tier ({band})', claim)

    views = unit.get('medianViews')
    posts = info.get('postsUsed')
    if unit.get('method') == 'views' and views:
        start = views / 1000 * unit['cpmUsd'] * unit['ratio']
        ratio = f" x {unit['ratio']:g}" if unit['ratio'] != 1 else ''
        add('Median views', f'{views:,.0f}' + (f' (last {posts} posts)' if posts else ''),
            f"${unit['cpmUsd']:g} per 1,000 views is the 2026 benchmark",
            f"{views:,.0f} / 1,000 x ${unit['cpmUsd']:g}{ratio} = {money(start)} starting price. Brands pay for views, so this is the core of the price.")
        if metrics.audience:
            reach = views / metrics.audience * 100
            add('Reach per post', f'{reach:.0f}% of {word}', 'Views divided by audience',
                f'Each post reaches {reach:.0f}% of your {word}: proof the audience is active, not just large.')
    elif unit.get('method') == 'follower_fallback':
        add('Median views', 'Not available', 'Priced from audience size instead',
            'No usable view counts, so the price uses a per-follower benchmark and confidence is lower.')

    er, bandr, adj = unit.get('engagementRate'), unit.get('engagementBand'), unit.get('erAdjustment') or 1.0
    if er is not None and bandr:
        lo, hi = bandr
        where = 'above' if er > hi else 'below' if er < lo else 'within'
        add('Engagement', f'{er * 100:.1f}%', f'Typical {lo * 100:.1f}% to {hi * 100:.1f}% for accounts this size',
            f'{where.capitalize()} the typical range: price x {adj:.2f}.')
    elif getattr(metrics, 'likes_hidden', False):
        add('Engagement', 'Likes hidden', 'No benchmark comparison possible', 'No engagement adjustment applied.')

    nm = unit.get('nicheMultiplier') or 1.0
    if niche:
        more = 'more' if nm > 1 else 'less' if nm < 1 else 'the same'
        add('Niche', niche.replace('_', ' ').title(), 'Lifestyle = x1.00',
            f'Brands in this niche pay {more}' + (f': price x {nm:.2f}.' if nm != 1 else '.'))

    if abs(mf - 1) > 0.005:
        add('Audience country', market.get('name', ''), 'US benchmarks = x1.00', f'Brands pay by audience location: price x {mf:.2f}.')

    sponsored = info.get('sponsoredPostsInSample')
    if sponsored and posts:
        add('Sponsored posts', f'{sponsored} of the last {posts}', 'Paid partnerships found in recent posts',
            'Brands already pay you: useful proof of sponsor fit in a pitch.')

    if getattr(metrics, 'volatility', None):
        add('View consistency', f'Top posts get {metrics.volatility:.1f}x the views of weak ones', 'Spread of recent views',
            'Less predictable reach: brands may push back, so lead with your median, not your best post.')

    add('Result', f'{money(unit["unitUsd"])} per {label}', 'Fair value for one post, before any rights or extras',
        'Every right and extra in the line items is priced on top of this.')
    return out
