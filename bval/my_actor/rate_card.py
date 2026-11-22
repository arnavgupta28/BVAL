"""No offer yet: what the creator should charge, from their own numbers.

Everything is priced by the same engine as a deal check (evaluate_deal), so the rate card, the packages and the
creator's own custom package always agree. The creator's custom package is the main price range of the run
(whatever they filled in); this module adds the recommendations around it:

- perPost: one piece of each format on the platform, no extra rights
- addOns: what each common extra adds on top of one main post
- packages: three ready-made bundles to pitch (Starter, Standard, Premium), with the usual package discount
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Callable

from .counter_email import deliverable_label
from .pricing import Metrics, PricingError, Terms, _na_set, evaluate_deal

MAIN = {'instagram': 'instagram_reel', 'tiktok': 'tiktok_video', 'youtube': 'youtube_integration'}
# Second format used in the Standard and Premium packages.
SECOND = {'instagram': ('instagram_story_frame', 3), 'tiktok': ('tiktok_video', 1), 'youtube': ('youtube_short', 1)}


def _bare(terms: Terms) -> Terms:
    """The creator's niche, market and contract terms, with no deliverables, rights or extras."""
    return replace(
        terms,
        deliverables=[],
        organic_usage_days=0, paid_usage_days=0, whitelisting_days=0, exclusivity_days=0, exclusivity_scope='category',
        perpetual_rights=False, rush_hours=0, revision_rounds=1, raw_footage=False, link_in_bio_days=0,
        story_link_sticker=False, pinned_comment_link=False, cross_post_platforms=0, ai_training_clause=False,
        ad_spend_usd=None, offer_amount=None, gifted_only=False,
    )


def _points(metrics: Metrics, terms: Terms, rates: dict) -> dict | None:
    try:
        return evaluate_deal(metrics, terms, rates)['pricePointsUsd']
    except PricingError:
        return None  # e.g. YouTube Shorts with no Shorts views: leave that format out


def build_rate_card(metrics: Metrics, terms: Terms, rates: dict, money: Callable[[float], str], exact: Callable[[float], float]) -> dict[str, Any]:
    platform = metrics.platform
    bare = _bare(terms)
    na = _na_set(platform, rates)
    main = MAIN[platform]

    def priced(pts: dict) -> dict:
        return {'fair': money(pts['fair']), 'ask': money(pts['ask']), 'floor': money(pts['floor']),
                'fairValue': exact(pts['fair']), 'askValue': exact(pts['ask']), 'floorValue': exact(pts['floor'])}

    per_post = []
    for dtype in rates['platforms'][platform]['deliverables']:
        if dtype in na:
            continue
        pts = _points(metrics, replace(bare, deliverables=[{'type': dtype, 'qty': 1}]), rates)
        if pts:
            per_post.append({'type': dtype, 'label': deliverable_label(dtype), **priced(pts)})

    one_main = replace(bare, deliverables=[{'type': main, 'qty': 1}])
    base = _points(metrics, one_main, rates)
    add_ons = []
    if base:
        # (key, label, change, rule name in rates "not_applicable")
        menu = [
            ('organic_usage_30', 'Brand can repost it, 30 days', {'organic_usage_days': 30}, 'organic_usage'),
            ('organic_usage_90', 'Brand can repost it, 90 days', {'organic_usage_days': 90}, 'organic_usage'),
            ('paid_usage_30', 'Brand runs it as its own ad, 30 days', {'paid_usage_days': 30}, 'paid_usage'),
            ('whitelisting_30', 'Ads through your handle, 30 days', {'whitelisting_days': 30}, 'whitelisting'),
            ('exclusivity_30', 'Category exclusivity, 30 days', {'exclusivity_days': 30}, 'exclusivity'),
            ('rush_48h', 'Rush delivery (48 hours)', {'rush_hours': 48}, 'rush'),
            ('raw_footage', 'Raw footage', {'raw_footage': True}, 'raw_footage'),
            ('link_in_bio_7', 'Link in bio, 7 days', {'link_in_bio_days': 7}, 'link_in_bio'),
            ('story_link_sticker', 'Story link sticker', {'story_link_sticker': True}, 'story_link_sticker'),
        ]
        for key, label, change, rule in menu:
            if rule in na:
                continue
            pts = _points(metrics, replace(one_main, **change), rates)
            if pts and pts['fair'] - base['fair'] > 0.5:
                add_ons.append({'key': key, 'label': label, 'adds': '+' + money(pts['fair'] - base['fair']),
                                'addsValue': exact(pts['fair'] - base['fair'])})

    second, second_qty = SECOND[platform]
    if second == main:
        main_extra, second_dels = 1, []
    else:
        main_extra, second_dels = 0, [{'type': second, 'qty': second_qty}] if second not in na else []
    ads = {'whitelisting_days': 30} if 'whitelisting' not in na else {'paid_usage_days': 30}
    plans = [
        ('Starter', [{'type': main, 'qty': 1}], {}),
        ('Standard', [{'type': main, 'qty': 1 + main_extra}] + second_dels, {'organic_usage_days': 30}),
        ('Premium', [{'type': main, 'qty': 2 + main_extra}] + second_dels,
         {'organic_usage_days': 30, **ads, 'exclusivity_days': 30}),
    ]
    packages = []
    for name, dels, rights in plans:
        pts = _points(metrics, replace(bare, deliverables=dels, **rights), rates)
        if not pts:
            pts = _points(metrics, replace(bare, deliverables=[d for d in dels if d['type'] == main], **rights), rates)
            dels = [d for d in dels if d['type'] == main]
        if not pts:
            continue
        includes = [f"{d['qty']} x {deliverable_label(d['type'])}" for d in dels]
        includes += _rights_text(rights)
        packages.append({'name': name, 'includes': includes, **priced(pts)})

    return {'perPost': per_post, 'addOns': add_ons, 'packages': packages}


def _rights_text(rights: dict) -> list[str]:
    out = []
    if rights.get('organic_usage_days'):
        out.append(f"brand can repost it for {rights['organic_usage_days']} days")
    if rights.get('whitelisting_days'):
        out.append(f"ads through your handle for {rights['whitelisting_days']} days")
    if rights.get('paid_usage_days'):
        out.append(f"brand ads for {rights['paid_usage_days']} days")
    if rights.get('exclusivity_days'):
        out.append(f"{rights['exclusivity_days']} days category exclusivity")
    return out
