"""Counter-offer email: LLM-written from structured JSON, with a deterministic template fallback.

The LLM only writes prose. Every number it may use is in the payload, computed by the pricing engine.
LLM calls go through Apify's OpenRouter proxy (billed to Apify credit, authenticated with APIFY_TOKEN).
Rules follow bval_research.md section 8 (Beacons / Elev8or negotiation guidance).
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import ssl
import urllib.error
import urllib.request
from typing import Any

OPENROUTER_URL = 'https://openrouter.apify.actor/api/v1/chat/completions'
DEFAULT_MODELS = ['anthropic/claude-sonnet-4.5', 'openai/gpt-4o-mini']

CURRENCY_SYMBOL = {'USD': '$', 'INR': '₹', 'GBP': '£', 'EUR': '€', 'BRL': 'R$', 'CAD': 'C$', 'AUD': 'A$', 'MXN': 'MX$', 'IDR': 'Rp', 'JPY': '¥', 'PHP': '₱'}

SYSTEM_PROMPT = """You write counter-offer emails for content creators replying to brand sponsorship offers.
Write in a friendly, confident, collaborative tone. 150-250 words, readable on a phone.

Hard rules:
- Use ONLY the numbers, prices, dates and facts in the input JSON. Never invent or recompute numbers.
- Never reveal the floor or walk-away price, the verdict code, or that a tool produced the numbers.
- Never lower the price without removing scope. Every usage right or exclusivity gets an end date.
- Never grant usage or exclusivity for gifted product. Never accept perpetual or AI-training rights at the base price.
- Push back on each red flag with one concrete alternative.

Structure:
1. Thanks + one line showing you read the brief.
2. Fit, backed by the single proof point given.
3. The itemised quote: each line item with its price.
4. Pushback on flagged terms (if any).
5. A two-option close using option_a and option_b when both are given ("Which works better on your side?").
6. Terms: the payment terms given.
7. Short sign-off with the creator's name.

Strategy by verdict:
- ACCEPT_STRONG / ACCEPT: accept warmly and restate deliverables, usage, exclusivity, fee and payment terms in writing.
- COUNTER_LIGHT: counter at option_a; signal flexibility on timing, not price.
- COUNTER_TRADE_SCOPE: full scope at option_a, or the reduced scope at option_b (describe option_b using its "changes" list).
- DECLINE_OR_REDUCE_SCOPE: decline the current terms warmly and offer only option_b (the reduced scope).
- NO_OFFER: send a quote at option_a, with option_b as a lighter alternative if given.

Write the email in the language given by "email_language" (ISO code). If a disclosure_note is given, add it as one short line.
Return ONLY JSON: {"subject": "...", "body": "..."}"""


DELIVERABLE_LABELS = {
    'instagram_reel': 'Instagram Reel',
    'instagram_story_frame': 'Instagram Story frame',
    'instagram_static_post': 'Instagram feed post',
    'instagram_carousel': 'Instagram carousel',
    'tiktok_video': 'TikTok video',
    'youtube_integration': 'YouTube integration (60-90s)',
    'youtube_mention_15_30s': 'YouTube mention (15-30s)',
    'youtube_dedicated': 'Dedicated YouTube video',
    'youtube_short': 'YouTube Short',
}

# How each traded-away term is described to the brand in the reduced-scope option.
REDUCTION_LABELS = {
    'rush': 'standard turnaround instead of rush',
    'revisions': 'one revision round',
    'raw_footage': 'no raw footage',
    'cross_post': 'no cross-posting',
    'paid_usage': 'no paid usage',
    'exclusivity': 'exclusivity limited to 7 days',
    'whitelisting': 'no ads through my handle',
    'link_in_bio': 'no link in bio',
    'story_link_sticker': 'no Story link sticker',
    'pinned_comment_link': 'description link only',
    'organic_usage': 'organic usage limited to 30 days',
}

# Brand-facing pushback for each red flag (the creator-facing explanations stay in the dataset).
FLAG_PUSHBACK = {
    'PERPETUAL_RIGHTS': 'Usage: I license content for a defined term. Happy to do 12 months with renewal options rather than perpetuity.',
    'UNPRICED_WHITELISTING': 'Ads through my handle are priced as a separate line, since they extend reach well beyond organic.',
    'USAGE_OVERBUY': 'Paid usage: short-form content peaks in the first weeks, so I would suggest a shorter window with renewals.',
    'LONG_EXCLUSIVITY': 'Exclusivity: a long category lock means turning down other partners, so it is priced as its own line. A shorter window brings the total down significantly.',
    'GIFTED_FOR_RIGHTS': 'Product-only collaborations do not include usage or exclusivity rights.',
    'AI_LIKENESS': 'I would like to remove the AI training / likeness clause, or discuss it separately.',
    'SLOW_PAY_NO_DEPOSIT': 'Payment: I work with a 50% deposit and Net 30.',
    'RUSH_UNPAID': 'Timeline: the fast turnaround is included as a rush line; a standard timeline removes it.',
    'EXCESS_REVISIONS': 'Revisions: one round is included; extra rounds are listed above.',
    'FREE_RAW_FOOTAGE': 'Raw footage is licensed as a separate line.',
    'BUNDLE_SQUEEZE': 'The package price already includes a multi-deliverable discount.',
}


def deliverable_label(dtype: str) -> str:
    return DELIVERABLE_LABELS.get(dtype, dtype.replace('_', ' '))


def format_money(usd: float, currency: str, fx: float, step: int) -> str:
    value = usd * fx
    value = round(value / step) * step if step else value
    sym = CURRENCY_SYMBOL.get(currency, currency + ' ')
    if currency == 'INR':
        s = f'{int(value):d}'
        head, tail = s[:-3], s[-3:]
        if head:
            head = re.sub(r'(\d)(?=(\d{2})+$)', r'\1,', head)
            return f'{sym}{head},{tail}'
        return f'{sym}{tail}'
    return f'{sym}{value:,.0f}'


def build_payload(result: dict, ctx: dict) -> dict:
    """Structured, number-complete input for the email writer. `ctx` carries display + identity info."""
    money = ctx['money']
    pts = result['pricePointsUsd']
    scope = result['scope']
    lines = [{'item': f"{u['qty']} x {deliverable_label(u['type'])}", 'price': money(u['subtotalUsd'])} for u in scope['units']]
    if scope['packageDiscountPct']:
        lines.append({'item': f"Package discount ({scope['packageDiscountPct']:.0f}%)", 'price': '-' + money(scope['grossUsd'] - scope['contentBaseUsd'])})
    lines += [{'item': a['item'], 'price': money(a['amountUsd']) if a['amountUsd'] else 'included'} for a in scope['addons']]

    reduced = result.get('reducedScope')
    option_b = None
    if reduced:
        option_b = {'price': money(reduced['priceUsd']), 'changes': [REDUCTION_LABELS.get(k, k.replace('_', ' ')) for k in reduced['droppedOrReduced']]}
    return {
        'creator_name': ctx.get('creator_name') or ctx['handle'],
        'brand_name': ctx.get('brand_name') or 'your team',
        'platform': ctx['platform'],
        'verdict': result['verdict'],
        'brand_offer': money(result['offerUsd']) if result.get('offerUsd') is not None else None,
        'proof_point': ctx.get('proof_point'),
        'line_items': lines,
        'total_quote': money(pts['ask']),
        'option_a': {'price': money(pts['ask']), 'scope': 'full requested scope'},
        'option_b': option_b,
        'red_flags': [FLAG_PUSHBACK[f['code']] for f in result['redFlags'] if f['code'] in FLAG_PUSHBACK],
        'payment_terms': '50% deposit on signing, balance Net 30; usage rights start on full payment.',
        'email_language': ctx.get('email_language', 'en'),
        'disclosure_note': ctx.get('disclosure_note'),
        'tax_note': ctx.get('tax_note'),
    }


def template_email(p: dict) -> dict:
    """Deterministic fallback used when the LLM is unavailable."""
    brand, name = p['brand_name'], p['creator_name']
    items = '\n'.join(f"- {li['item']}: {li['price']}" for li in p['line_items'])
    flags = ''
    if p['red_flags']:
        flags = '\nA few notes on the terms:\n' + '\n'.join(f'- {f}' for f in p['red_flags']) + '\n'
    v = p['verdict']
    lighter = f"({'; '.join(p['option_b']['changes'])})" if p['option_b'] else ''
    if v in ('ACCEPT', 'ACCEPT_STRONG'):
        ask = f"Happy to confirm at {p['brand_offer']} for the scope below."
        close = 'If that all looks right, send over the agreement and we can lock dates.'
    elif v == 'DECLINE_OR_REDUCE_SCOPE' and p['option_b']:
        ask = f"I can't take on the full scope at {p['brand_offer']}, but I'd love to make something work. For reference, the full scope prices out as follows:"
        close = f"Within your budget range, I can offer a lighter version {lighter} for {p['option_b']['price']}. Would that work on your side?"
    else:
        ask = f"For the full scope, my rate is {p['option_a']['price']}."
        close = (
            f"If budget is fixed, I can do a lighter version {lighter} for {p['option_b']['price']}. Which works better on your side?"
            if p['option_b']
            else 'Let me know if that works and I will send the agreement.'
        )
    proof = f"\n{p['proof_point']}\n" if p.get('proof_point') else ''
    tax = f"\n{p['tax_note']}" if p.get('tax_note') else ''
    body = (
        f"Hi {brand} team,\n\nThanks so much for reaching out. I really like the brief and think it's a great fit for my audience.\n"
        f"{proof}\n{ask}\n\nHere's the breakdown:\n{items}\n{flags}\n{close}\n\n"
        f"Terms: {p['payment_terms']}{tax}\n\nBest,\n{name}"
    )
    return {'subject': f"Re: {brand} x {name} partnership", 'body': body}


def _ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    # python.org builds on macOS ship without root certificates; use the system bundle when present.
    for path in ('/etc/ssl/cert.pem', '/etc/ssl/certs/ca-certificates.crt'):
        if os.path.exists(path):
            ctx.load_verify_locations(cafile=path)
            break
    return ctx


def _post(url: str, token: str, payload: dict, timeout: int = 45) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:  # noqa: S310 (fixed https URL)
        return json.loads(resp.read().decode())


def _parse(content: str) -> dict | None:
    m = re.search(r'\{.*\}', content or '', re.S)
    if not m:
        return None
    try:
        out = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if isinstance(out.get('subject'), str) and isinstance(out.get('body'), str) and len(out['body']) > 80:
        return {'subject': out['subject'].strip(), 'body': out['body'].strip()}
    return None


async def write_email(payload: dict, model: str | None = None, log: Any = None) -> tuple[dict, str]:
    """Return (email, generated_by). generated_by is the model slug, or 'template'."""
    token = os.environ.get('APIFY_TOKEN')
    if not token:
        return template_email(payload), 'template'
    models = [model] if model else []
    models += [m for m in DEFAULT_MODELS if m not in models]
    for slug in models:
        try:
            data = await asyncio.to_thread(
                _post,
                OPENROUTER_URL,
                token,
                {
                    'model': slug,
                    'temperature': 0.4,
                    'max_tokens': 900,
                    'messages': [
                        {'role': 'system', 'content': SYSTEM_PROMPT},
                        {'role': 'user', 'content': json.dumps(payload, ensure_ascii=False)},
                    ],
                },
            )
            email = _parse(data['choices'][0]['message']['content'])
            if email:
                return email, slug
            if log:
                log.warning(f'LLM {slug} returned an unusable email; trying the next option.')
        except urllib.error.HTTPError as e:
            if log:
                detail = e.read().decode(errors='replace')[:300] if hasattr(e, 'read') else ''
                log.warning(f'LLM {slug} failed (HTTP {e.code}: {detail}); trying the next option.')
        except (urllib.error.URLError, KeyError, IndexError, TimeoutError, json.JSONDecodeError) as e:
            if log:
                log.warning(f'LLM {slug} failed ({type(e).__name__}: {e}); trying the next option.')
    return template_email(payload), 'template'
