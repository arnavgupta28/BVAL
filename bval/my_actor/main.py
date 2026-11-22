"""BVAL: brand-deal valuation for creators.

Input: a creator handle + the brand's deal terms. Output: a fair rate, itemised add-ons, a walk-away/floor/fair/ask
range, a verdict on the brand's offer, red flags, and a ready-to-send counter-offer email.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from apify import Actor, Event

from .counter_email import build_payload, deliverable_label, format_money, write_email
from .feeders import FeederError, clean_handle, scrape
from .pricing import DISCLAIMER, Metrics, PricingError, Terms, evaluate_deal, load_rates, resolve_market

PLATFORM_DEFAULT_DELIVERABLE = {'instagram': 'instagram_reel', 'tiktok': 'tiktok_video', 'youtube': 'youtube_integration'}


def _int(v: Any, default: int = 0) -> int:
    try:
        return int(v) if v is not None and v != '' else default
    except (TypeError, ValueError):
        return default


def build_terms(inp: dict, market: dict) -> Terms:
    platform = inp.get('platform', 'instagram')
    deliverables = inp.get('deliverables') or [{'type': PLATFORM_DEFAULT_DELIVERABLE[platform], 'qty': 1}]
    return Terms(
        deliverables=[{'type': str(d.get('type')), 'qty': _int(d.get('qty'), 1)} for d in deliverables if isinstance(d, dict)],
        niche=inp.get('niche', 'lifestyle'),
        organic_usage_days=_int(inp.get('organicUsageDays')),
        paid_usage_days=_int(inp.get('paidUsageDays')),
        whitelisting_days=_int(inp.get('whitelistingDays')),
        exclusivity_days=_int(inp.get('exclusivityDays')),
        exclusivity_scope=inp.get('exclusivityScope', 'category'),
        perpetual_rights=bool(inp.get('perpetualRights')),
        rush_hours=_int(inp.get('rushHours')),
        revision_rounds=_int(inp.get('revisionRounds'), 1),
        raw_footage=bool(inp.get('rawFootage')),
        link_in_bio_days=_int(inp.get('linkInBioDays')),
        story_link_sticker=bool(inp.get('storyLinkSticker')),
        pinned_comment_link=bool(inp.get('pinnedCommentLink')),
        cross_post_platforms=_int(inp.get('crossPostPlatforms')),
        payment_terms_days=_int(inp.get('paymentTermsDays'), 30),
        deposit_pct=_int(inp.get('depositPct'), 50),
        ai_training_clause=bool(inp.get('aiTrainingClause')),
        ad_spend_usd=inp.get('adSpendUsd') or None,
        offer_amount=inp.get('offerAmount') if inp.get('offerAmount') not in (None, '') else None,
        offer_currency=(inp.get('offerCurrency') or 'USD').upper(),
        gifted_only=bool(inp.get('giftedOnly')),
        market=market['code'],
    )


def manual_metrics(platform: str, mm: dict) -> Metrics:
    anchor = {'instagram': 'instagram_reel', 'tiktok': 'tiktok_video', 'youtube': 'youtube_integration'}[platform]
    views = {anchor: mm.get('medianViews')}
    er = {anchor: mm.get('engagementRate')}
    if platform == 'youtube' and mm.get('medianShortsViews'):
        views['youtube_short'] = mm['medianShortsViews']
    return Metrics(
        platform=platform,
        audience=_int(mm.get('followers')) or None,
        median_views=views,
        engagement_rate=er,
        sample_size={k: 30 for k in views},
        source='manual',
    )


def proof_point(platform: str, m: Metrics) -> str | None:
    anchor = {'instagram': 'instagram_reel', 'tiktok': 'tiktok_video', 'youtube': 'youtube_integration'}[platform]
    v, er = m.median_views.get(anchor), m.engagement_rate.get(anchor)
    if not v:
        return None
    noun = {'instagram': 'Reels reach', 'tiktok': 'videos reach', 'youtube': 'videos (30+ days old) average'}[platform]
    s = f'My recent {noun} a median of {v:,.0f} views'
    if er:
        s += f' with {er * 100:.1f}% engagement'
    return s + '.'


def markdown_report(item: dict) -> str:
    p = item['priceRange']
    lines = [
        f"# BVAL deal check: @{item['handle']} ({item['platform']})",
        '',
        f"**Verdict: {item['verdict'].replace('_', ' ')}.** {item['verdictText']}",
        '',
        '| Walk-away | Floor | Fair | Ask | Brand offer |',
        '|---|---|---|---|---|',
        f"| {p['walkAway']} | {p['floor']} | **{p['fair']}** | {p['ask']} | {item.get('offerDisplay') or '-'} |",
        '',
        '## Line items',
        '',
        '| Item | Amount | Source |',
        '|---|---|---|',
    ]
    for li in item['lineItems']:
        src = 'assumption' if li['isAssumption'] else ', '.join(li['sources'])
        lines.append(f"| {li['item']} | {li['amount']} | {src} |")
    if item['redFlags']:
        lines += ['', '## Red flags', ''] + [f"- **{f['code']}**: {f['message']}" for f in item['redFlags']]
    if item.get('counterOptions', {}).get('reducedScope'):
        rs = item['counterOptions']['reducedScope']
        lines += ['', f"**Reduced-scope option:** {rs['price']} (drops or reduces: {', '.join(rs['dropped'])})"]
    m = item['metrics']
    lines += [
        '',
        '## Data used',
        '',
        f"Audience {m['audience'] or 0:,} ({m['tier']} tier), median views {m['medianViews'] or 0:,.0f}, "
        f"engagement {(m['engagementRate'] or 0) * 100:.1f}%, "
        + (f"{m['postsUsed']} posts analysed" if m['postsUsed'] else 'metrics supplied manually')
        + f". Confidence: **{item['confidence']}**" + (f" ({'; '.join(item['confidenceReasons'])})" if item['confidenceReasons'] else ''),
    ]
    if item.get('counterEmail'):
        lines += ['', '## Counter-offer email', '', f"**Subject:** {item['counterEmail']['subject']}", '', item['counterEmail']['body']]
    lines += ['', f"_{item['disclaimer']} Rates version {item['ratesVersion']}._"]
    return '\n'.join(lines)


async def main() -> None:
    async with Actor:

        async def on_aborting(_: Any = None) -> None:
            await Actor.exit()

        Actor.on(Event.ABORTING, on_aborting)

        inp = await Actor.get_input() or {}
        rates = load_rates()
        platform = inp.get('platform', 'instagram')
        raw_handle = inp.get('handle', '')

        try:
            market = resolve_market(inp.get('market'), rates, platform)
            terms = build_terms(inp, market)
            handle = clean_handle(raw_handle)
            mm = inp.get('manualMetrics') or {}
            if mm.get('medianViews') or mm.get('followers'):
                metrics, info = manual_metrics(platform, mm), {'postsUsed': None, 'sponsoredPostsInSample': None}
            else:
                want_shorts = any(d['type'] == 'youtube_short' for d in terms.deliverables)
                Actor.log.info(f'Scraping @{handle} on {platform}...')
                metrics, info = await scrape(platform, handle, want_shorts=want_shorts)
            result = evaluate_deal(metrics, terms, rates)
        except (FeederError, PricingError) as e:
            Actor.log.error(str(e))
            await Actor.push_data({'handle': raw_handle, 'platform': platform, 'error': str(e)})
            await Actor.fail(status_message=str(e))
            return

        # Display currency
        out_cur, fx, step = 'USD', 1.0, 10
        if (inp.get('outputCurrency') or 'USD').upper() == 'LOCAL' and market['currency'] != 'USD':
            out_cur, fx, step = market['currency'], market['fx_per_usd'], market['rounding']
        money = lambda usd: format_money(usd, out_cur, fx, step)  # noqa: E731
        exact = lambda usd: round(usd * fx, 2)  # noqa: E731

        pts = result['pricePointsUsd']
        scope = result['scope']
        anchor = scope['units'][0]['anchor']
        line_items = []
        for u in scope['units']:
            line_items.append({
                'item': f"{u['qty']} x {deliverable_label(u['type'])}",
                'kind': 'deliverable',
                'amount': money(u['subtotalUsd']),
                'amountValue': exact(u['subtotalUsd']),
                'sources': ['see rates.json'],
                'isAssumption': False,
                'detail': {k: u[k] for k in ('method', 'medianViews', 'cpmUsd', 'ratio', 'nicheMultiplier', 'erAdjustment', 'clamped', 'marketFactor') if k in u},
            })
        if scope['packageDiscountPct']:
            line_items.append({
                'item': f"Package discount ({scope['packageDiscountPct']:.0f}%)",
                'kind': 'discount',
                'amount': '-' + money(scope['grossUsd'] - scope['contentBaseUsd']),
                'amountValue': -exact(scope['grossUsd'] - scope['contentBaseUsd']),
                'sources': ['package_discounts_pct'],
                'isAssumption': False,
            })
        for a in scope['addons']:
            line_items.append({
                'item': a['item'],
                'kind': 'addon',
                'pctOfBase': a['pctOfBase'],
                'amount': money(a['amountUsd']) if a['amountUsd'] else 'included',
                'amountValue': exact(a['amountUsd']),
                'sources': a['sources'],
                'isAssumption': a['isAssumption'],
            })

        reduced = result.get('reducedScope')
        item: dict[str, Any] = {
            'handle': handle,
            'platform': platform,
            'creatorName': info.get('displayName'),
            'niche': terms.niche,
            'market': market['code'],
            'marketName': market['name'],
            'currency': out_cur,
            'verdict': result['verdict'],
            'verdictText': result['verdictText'],
            'offerAmount': terms.offer_amount,
            'offerCurrency': terms.offer_currency,
            'offerDisplay': money(result['offerUsd']) if result.get('offerUsd') is not None else None,
            'gapPct': round(result['gapPct'], 1) if result.get('gapPct') is not None else None,
            'fairPrice': exact(pts['fair']),
            'askPrice': exact(pts['ask']),
            'floorPrice': exact(pts['floor']),
            'walkAwayPrice': exact(pts['walkAway']),
            'priceRange': {k: money(v) for k, v in pts.items()},
            'lineItems': line_items,
            'counterOptions': {
                'fullScope': {'price': money(pts['ask']), 'scope': 'everything the brand requested'},
                'reducedScope': {'price': money(reduced['priceUsd']), 'dropped': reduced['droppedOrReduced']} if reduced else None,
            },
            'redFlags': result['redFlags'],
            'warnings': result['warnings'] + market.get('warnings', []),
            'metrics': {
                'audience': metrics.audience,
                'tier': result['tier'],
                'medianViews': metrics.median_views.get(anchor),
                'engagementRate': round(metrics.engagement_rate[anchor], 4) if metrics.engagement_rate.get(anchor) else None,
                'postsUsed': info.get('postsUsed'),
                'viewsField': metrics.views_field,
                'volatility': round(metrics.volatility, 2) if metrics.volatility else None,
                'sponsoredPostsInSample': info.get('sponsoredPostsInSample'),
                'source': metrics.source,
            },
            'confidence': result['confidence'],
            'confidenceReasons': result['confidenceReasons'],
            'taxNote': market.get('tax_note'),
            'disclaimer': DISCLAIMER,
            'ratesVersion': result['ratesVersion'],
            'evaluatedAt': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        }

        charge = 'manual-deal-evaluated' if metrics.source == 'manual' else 'deal-evaluated'
        await Actor.charge(event_name=charge)

        if inp.get('generateEmail', True):
            ctx = {
                'money': money,
                'handle': handle,
                'creator_name': inp.get('creatorName') or info.get('displayName'),
                'brand_name': inp.get('brandName'),
                'platform': platform,
                'proof_point': proof_point(platform, metrics),
                'email_language': market.get('email_language', 'en'),
                'disclosure_note': market.get('disclosure'),
                'tax_note': market.get('tax_note'),
            }
            payload = build_payload(result, ctx)
            email, generated_by = await write_email(payload, model=inp.get('llmModel') or None, log=Actor.log)
            item['counterEmail'] = email
            item['emailGeneratedBy'] = generated_by
            await Actor.charge(event_name='counter-email-drafted')

        report = markdown_report(item)
        await Actor.set_value('QUOTE.md', report, content_type='text/markdown')
        await Actor.push_data(item)
        Actor.log.info(f"@{handle}: fair {item['priceRange']['fair']}, verdict {item['verdict']}.")


if __name__ == '__main__':
    asyncio.run(main())
