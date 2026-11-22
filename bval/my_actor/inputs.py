"""Input normalisation: the grouped (nested) input schema -> the flat field names the rest of the code reads.

The input form groups fields the way a creator thinks about a deal (mentor feedback: mandatory vs optional,
grouped, hierarchical, self-explanatory):

    platform*, handle*             who is being priced (the only required fields)
    niche, market                  what kind of creator, whose audience
    offer {brandName, amount, currency, productOnly}
    deliverables [{type, qty}]
    rights {organicUsageDays, paidUsageDays, whitelistingDays, adSpendUsd, perpetualRights, exclusivityDays, exclusivityScope}
    extras {rushHours, revisionRounds, rawFootage, crossPostPlatforms, linkInBioDays, storyLinkSticker, pinnedCommentLink}
    contract {paymentTermsDays, depositPct, aiTrainingClause}
    outputCurrency, generateEmail, creatorName, sendReportTo, manualMetrics, llmModel

Older flat inputs (offerAmount, organicUsageDays, ...) are still accepted, so saved tasks, API callers and agents
using the earlier field names keep working. When both are given, the grouped value wins.
"""

from __future__ import annotations

from typing import Any

# group -> {sub-field: flat field name}
GROUPS: dict[str, dict[str, str]] = {
    'offer': {'brandName': 'brandName', 'amount': 'offerAmount', 'currency': 'offerCurrency', 'productOnly': 'giftedOnly', 'noOffer': 'noOffer'},
    'rights': {
        'organicUsageDays': 'organicUsageDays',
        'paidUsageDays': 'paidUsageDays',
        'whitelistingDays': 'whitelistingDays',
        'adSpendUsd': 'adSpendUsd',
        'perpetualRights': 'perpetualRights',
        'exclusivityDays': 'exclusivityDays',
        'exclusivityScope': 'exclusivityScope',
    },
    'extras': {
        'rushHours': 'rushHours',
        'revisionRounds': 'revisionRounds',
        'rawFootage': 'rawFootage',
        'crossPostPlatforms': 'crossPostPlatforms',
        'linkInBioDays': 'linkInBioDays',
        'storyLinkSticker': 'storyLinkSticker',
        'pinnedCommentLink': 'pinnedCommentLink',
    },
    'contract': {'paymentTermsDays': 'paymentTermsDays', 'depositPct': 'depositPct', 'aiTrainingClause': 'aiTrainingClause'},
}


def normalize_input(raw: dict[str, Any] | None) -> dict[str, Any]:
    """Return a flat input dict. Grouped values override flat ones; empty strings count as 'not given'."""
    inp = dict(raw or {})
    for group, mapping in GROUPS.items():
        sub = inp.get(group)
        if not isinstance(sub, dict):
            continue
        for key, flat in mapping.items():
            value = sub.get(key)
            if value is not None and value != '':
                inp[flat] = value
    # Deliverables: drop empty rows the form may leave behind; default qty 1.
    dels = inp.get('deliverables')
    if isinstance(dels, list):
        inp['deliverables'] = [
            {'type': d['type'], 'qty': d.get('qty') or 1} for d in dels if isinstance(d, dict) and d.get('type')
        ]
    if isinstance(inp.get('handle'), str):
        inp['handle'] = inp['handle'].strip()
    return inp
