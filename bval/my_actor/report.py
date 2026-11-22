"""Two renderings of one deal result: a short agent-facing summary, and human-facing reports (HTML and Markdown).

All three read the same dataset item, so they never disagree. Scraped values (display name, handle) are
untrusted: every value goes through html.escape before it reaches the HTML page.

Visual style (report and email): near-black or light-grey canvas, bright solid cards in lime, yellow, pink,
blue and lilac with black text, 24-28px corners, white pill buttons, a wide display font, plus drawn
figures (an avatar per creator, starbursts, sparkles, squiggle lines). See assets/design for the references.
"""

from __future__ import annotations

import hashlib
import math
from html import escape
from typing import Any

NEXT_ACTION = {
    'ACCEPT_STRONG': 'accept',
    'ACCEPT': 'accept',
    'COUNTER_LIGHT': 'counter',
    'COUNTER_TRADE_SCOPE': 'counter',
    'DECLINE_OR_REDUCE_SCOPE': 'decline',
    'NO_OFFER': 'quote',
}

VERDICT_LABEL = {
    'ACCEPT_STRONG': 'Accept: strong offer',
    'ACCEPT': 'Accept',
    'COUNTER_LIGHT': 'Counter',
    'COUNTER_TRADE_SCOPE': 'Counter or trade scope',
    'DECLINE_OR_REDUCE_SCOPE': 'Decline or reduce scope',
    'NO_OFFER': 'Your quote',
}

# Bright card colours from the design references. Text on them is always INK_DARK.
LIME, YELLOW, PINK, BLUE, LILAC = '#3BE36B', '#F4EE3E', '#F26CB5', '#3D8BFF', '#A68CF7'
INK_DARK = '#0B0B0C'
TONE = {'accept': LIME, 'counter': YELLOW, 'decline': PINK, 'quote': BLUE}
FONTS = 'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Unbounded:wght@500;700&display=swap'
BODY_FONT = "'Space Grotesk',-apple-system,'Segoe UI',Arial,sans-serif"
GLASS_CHIP = 'background:rgba(255,255,255,.38);border:1px solid rgba(255,255,255,.65)'
GLASS_CHIP_DARK = 'background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16)'
GLASS_DARK, GLASS_DARK_EDGE = 'rgba(255,255,255,.06)', 'rgba(255,255,255,.12)'
DISPLAY_FONT = "'Unbounded','Space Grotesk',-apple-system,'Segoe UI',Arial,sans-serif"


def next_action(verdict: str) -> str:
    return NEXT_ACTION.get(verdict, 'quote')


def _human(key: str) -> str:
    return key.replace('_', ' ')


def summary_line(item: dict) -> str:
    """One sentence an agent can relay as is: what to do, at what price, and why."""
    p, offer, action = item['priceRange'], item.get('offerDisplay'), next_action(item['verdict'])
    gap = item.get('gapPct')
    if action == 'accept':
        s = f"Accept: the offer of {offer} is at or above fair value ({p['fair']})."
    elif action == 'counter':
        s = f"Counter at {p['ask']}: the offer of {offer} is {gap:.0f}% below fair value ({p['fair']})."
    elif action == 'decline':
        s = f"Decline or cut scope: the offer of {offer} is below the walk-away point ({p['walkAway']}); fair value is {p['fair']}."
    else:
        s = f"No offer yet: quote {p['ask']} for this package (fair {p['fair']}, don't go below {p['floor']})."
        packs = (item.get('rateCard') or {}).get('packages') or []
        if packs:
            s += ' Ready-made packages: ' + ', '.join(f"{pk['name']} {pk['ask']}" for pk in packs) + '.'
    rs = (item.get('counterOptions') or {}).get('reducedScope')
    if rs and action in ('counter', 'decline'):
        s += f" Or offer reduced scope at {rs['price']} by dropping {', '.join(_human(d) for d in rs['dropped'])}."
    if item.get('redFlags'):
        s += f" Red flags: {', '.join(f['code'] for f in item['redFlags'])}."
    return s


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
    lines += _rate_card_md(item) + _evidence_md(item)
    lines += ['', '## Data used', '', _data_used(item)]
    if item.get('counterEmail'):
        lines += ['', '## Counter-offer email', '', f"**Subject:** {item['counterEmail']['subject']}", '', item['counterEmail']['body']]
    lines += ['', f"_{item['disclaimer']} Rates version {item['ratesVersion']}._"]
    return '\n'.join(lines)


def _data_used(item: dict) -> str:
    m = item['metrics']
    return (
        f"Audience {m['audience'] or 0:,} ({m['tier']} tier), median views {m['medianViews'] or 0:,.0f}, "
        f"engagement {(m['engagementRate'] or 0) * 100:.1f}%, "
        + (f"{m['postsUsed']} posts analysed" if m['postsUsed'] else 'metrics supplied manually')
        + f". Confidence: {item['confidence']}" + (f" ({'; '.join(r.rstrip('.') for r in item['confidenceReasons'])})" if item['confidenceReasons'] else '') + '.'
    )


def _evidence_html(item: dict) -> str:
    """'Your numbers': each stat BVAL pulled, the benchmark it was compared to, and what it did to the price."""
    ev = item.get('evidence') or []
    if not ev:
        return ''
    rows = ''.join(
        f'<li><div class="ev-top"><span>{escape(e["stat"])}</span><b>{escape(e["value"])}</b></div>'
        f'<small>{escape(e["benchmark"])}</small><p>{escape(e["claim"])}</p></li>'
        for e in ev
    )
    return f'<section id="numbers"><h2>Your numbers, and what they prove</h2><ul class="ev">{rows}</ul></section>'


def _rate_card_html(item: dict) -> str:
    """No offer yet: recommended packages, price per post and what each extra adds."""
    rc = item.get('rateCard')
    if not rc:
        return ''
    colours = ['g', 'y', 'l']
    packs = ''.join(
        f'<div class="tile {colours[i % 3]}">{sparkle("mini") if i == 2 else ""}<span>{escape(pk["name"])}</span>'
        f'<b>{escape(pk["ask"])}</b><small>fair {escape(pk["fair"])} · {escape(", ".join(pk["includes"]))}</small></div>'
        for i, pk in enumerate(rc.get('packages') or [])
    )
    per_post = ''.join(
        f'<tr><td>{escape(r["label"])}</td><td class="num">{escape(r["ask"])}</td><td class="src">fair {escape(r["fair"])}</td></tr>'
        for r in rc.get('perPost') or []
    )
    adds = ''.join(f'<tr><td>{escape(a["label"])}</td><td class="num">{escape(a["adds"])}</td></tr>' for a in rc.get('addOns') or [])
    out = '<section class="plain" id="rates"><h2>What to charge: ready-made packages</h2>'
    out += f'<div class="opts rc-packs">{packs}</div></section>' if packs else '</section>'
    if per_post:
        out += f'<section><h2>Price per post</h2><table>{per_post}</table><p class="note">Quote the first price; the fair price is where you can settle.</p></section>'
    if adds:
        out += f'<section><h2>What each extra adds</h2><table>{adds}</table><p class="note">On top of one main post. Mix and match to build your own package.</p></section>'
    return out


def _evidence_md(item: dict) -> list[str]:
    ev = item.get('evidence') or []
    if not ev:
        return []
    lines = ['', '## Your numbers, and what they prove', '', '| Stat | Value | Benchmark | What it means |', '|---|---|---|---|']
    lines += [f"| {e['stat']} | {e['value']} | {e['benchmark']} | {e['claim']} |" for e in ev]
    return lines


def _rate_card_md(item: dict) -> list[str]:
    rc = item.get('rateCard')
    if not rc:
        return []
    lines = ['', '## What to charge', '', '| Package | Quote | Fair | Includes |', '|---|---|---|---|']
    lines += [f"| {pk['name']} | {pk['ask']} | {pk['fair']} | {', '.join(pk['includes'])} |" for pk in rc.get('packages') or []]
    if rc.get('perPost'):
        lines += ['', '| Per post | Quote | Fair |', '|---|---|---|'] + [f"| {r['label']} | {r['ask']} | {r['fair']} |" for r in rc['perPost']]
    if rc.get('addOns'):
        lines += ['', '| Extra (on one main post) | Adds |', '|---|---|'] + [f"| {a['label']} | {a['adds']} |" for a in rc['addOns']]
    return lines


# ---------------------------------------------------------------------------------------------------------
# Drawn figures. All inline SVG built from numbers only, so no scraped text ever lands inside them.
# ---------------------------------------------------------------------------------------------------------

def _star_points(spikes: int, outer: float, inner: float, cx: float = 50, cy: float = 50) -> str:
    pts = []
    for i in range(spikes * 2):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / spikes - math.pi / 2
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return ' '.join(pts)


def burst(cls: str = 'burst', spikes: int = 12, inner: float = 7, outline: bool = False) -> str:
    """Spiky starburst like the campaign card and the onboarding screen."""
    paint = 'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"' if outline else 'fill="currentColor"'
    return f'<svg class="{cls}" viewBox="0 0 100 100" aria-hidden="true"><polygon points="{_star_points(spikes, 48, inner)}" {paint}/></svg>'


def sparkle(cls: str = 'sparkle') -> str:
    return (f'<svg class="{cls}" viewBox="0 0 40 40" aria-hidden="true"><path d="M20 0C21 13 27 19 40 20C27 21 21 27 20 40'
            'C19 27 13 21 0 20C13 19 19 13 20 0Z" fill="currentColor"/></svg>')


def squiggle(cls: str = 'squiggle') -> str:
    """Hand-drawn activity line like the 'Leads activity' tile."""
    return (f'<svg class="{cls}" viewBox="0 0 120 40" aria-hidden="true"><path d="M2 30C14 30 16 12 28 12S42 34 56 30 70 6 82 10'
            ' 96 32 118 8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>')


SKIN = ('#F6CFAF', '#E6AE85', '#C98C5F', '#9A6440', '#6B4329')
HAIR = ('#1B1B1D', '#3A2418', '#F2C94C', '#3BE36B', '#F26CB5')


def avatar_svg(seed: str, size: int = 72) -> str:
    """A cartoon creator avatar, the same one every time for the same handle.

    Rounded colour tile, head, eyes with highlights, brows, cheeks, grin, gold chain, and one of three
    headwear styles (beanie, cap, space buns) in the spirit of the 3D avatar references.
    """
    h = hashlib.sha256(seed.lower().encode()).digest()
    palette = [LIME, YELLOW, PINK, BLUE, LILAC]
    order = sorted(range(5), key=lambda i: h[i])
    bg, shirt, hat = (palette[i] for i in order[:3])
    skin, hair, style = SKIN[h[5] % 5], HAIR[h[6] % 5], h[7] % 3
    cid = f'av{h.hex()[:8]}'
    if style == 0:  # beanie with folded band and patch
        head = (f'<path d="M27 40C27 12 73 12 73 40Z" fill="{hat}"/>'
                f'<rect x="25" y="31" width="50" height="11" rx="5.5" fill="{hat}"/>'
                '<rect x="25" y="31" width="50" height="11" rx="5.5" fill="#000" opacity=".14"/>'
                f'<rect x="44" y="33.5" width="12" height="6" rx="2" fill="{INK_DARK}"/><rect x="47" y="35.5" width="6" height="2" rx="1" fill="{YELLOW}"/>')
    elif style == 1:  # backwards-free cap with brim and button
        head = (f'<path d="M24 40C23 33 26 33 30 35C30 23 40 22 50 22C60 22 70 23 70 35C74 33 77 33 76 40Z" fill="{hair}"/>'
                f'<path d="M29 37C29 15 71 15 71 37Z" fill="{hat}"/>'
                f'<path d="M30 35Q55 30 86 37Q84 43 70 41Q50 39 30 40Z" fill="{hat}"/>'
                '<path d="M30 35Q55 30 86 37Q84 43 70 41Q50 39 30 40Z" fill="#000" opacity=".18"/>'
                f'<circle cx="50" cy="17" r="2.6" fill="{INK_DARK}"/>')
    else:  # space buns with hair ties
        head = (f'<circle cx="31" cy="22" r="10" fill="{hair}"/><circle cx="69" cy="22" r="10" fill="{hair}"/>'
                f'<rect x="33" y="27" width="7" height="4" rx="2" fill="{hat}" transform="rotate(-35 36 29)"/>'
                f'<rect x="60" y="27" width="7" height="4" rx="2" fill="{hat}" transform="rotate(35 64 29)"/>'
                f'<path d="M28 44C26 20 74 20 72 44C66 34 58 30 50 33C42 30 34 34 28 44Z" fill="{hair}"/>')
    grin = ('<path d="M42 57Q50 67 58 57Z" fill="#1A1112"/><path d="M43.5 57.6Q50 59.6 56.5 57.6L56 59Q50 61 44 59Z" fill="#fff"/>'
            if h[8] % 2 else '<path d="M43 58Q50 64 57 58" fill="none" stroke="#1A1112" stroke-width="2.6" stroke-linecap="round"/>')
    return (
        f'<svg class="avatar" width="{size}" height="{size}" viewBox="0 0 100 100" role="img" aria-label="Creator avatar">'
        f'<defs><clipPath id="{cid}"><rect width="100" height="100" rx="28"/></clipPath>'
        f'<radialGradient id="{cid}g" cx="35%" cy="25%" r="80%"><stop offset="0" stop-color="#fff" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>'
        f'<g clip-path="url(#{cid})"><rect width="100" height="100" fill="{bg}"/><rect width="100" height="100" fill="url(#{cid}g)"/>'
        f'<path d="M12 106C14 82 30 73 50 73S86 82 88 106Z" fill="{shirt}"/>'
        f'<path d="M36 76Q50 84 64 76" fill="none" stroke="{INK_DARK}" stroke-width="3" opacity=".85"/>'
        f'<rect x="43" y="60" width="14" height="16" rx="6" fill="{skin}"/>'
        f'<path d="M38 74Q50 86 62 74" fill="none" stroke="#F2C94C" stroke-width="2.6"/><circle cx="50" cy="81" r="3.6" fill="#F2C94C"/>'
        f'<circle cx="29" cy="49" r="5" fill="{skin}"/><circle cx="71" cy="49" r="5" fill="{skin}"/>'
        f'<circle cx="71" cy="54" r="1.8" fill="#F2C94C"/>'
        f'<ellipse cx="50" cy="46" rx="21" ry="23" fill="{skin}"/>'
        f'{head}'
        '<path d="M37 42.5L46 43.5M54 43.5L63 42.5" stroke="#1A1112" stroke-width="2.8" stroke-linecap="round"/>'
        '<ellipse cx="42" cy="50" rx="4.4" ry="5" fill="#fff"/><ellipse cx="58" cy="50" rx="4.4" ry="5" fill="#fff"/>'
        f'<circle cx="42.6" cy="50.6" r="2.7" fill="{INK_DARK}"/><circle cx="58.6" cy="50.6" r="2.7" fill="{INK_DARK}"/>'
        '<circle cx="43.5" cy="49.4" r="1" fill="#fff"/><circle cx="59.5" cy="49.4" r="1" fill="#fff"/>'
        f'<circle cx="36" cy="57" r="3.2" fill="{PINK}" opacity=".45"/><circle cx="64" cy="57" r="3.2" fill="{PINK}" opacity=".45"/>'
        f'{grin}</g></svg>'
    )


def _range_bar(item: dict) -> str:
    pts = [('Walk-away', item['walkAwayPrice']), ('Floor', item['floorPrice']), ('Fair', item['fairPrice']), ('Ask', item['askPrice'])]
    offer = item.get('offerValue')
    values = [v for _, v in pts] + ([offer] if offer is not None else [])
    lo, hi = min(values) * 0.85, max(values) * 1.08
    pos = lambda v: max(0.0, min(100.0, (v - lo) / (hi - lo) * 100)) if hi > lo else 50.0  # noqa: E731
    p = item['priceRange']
    labels = {'Walk-away': p['walkAway'], 'Floor': p['floor'], 'Fair': p['fair'], 'Ask': p['ask']}
    # Labels alternate between two rows so neighbouring prices (often floor and fair) never overlap on a phone.
    ticks = ''.join(
        f'<div class="tick{" fair" if name == "Fair" else ""}{" low" if i % 2 else ""}" style="left:{pos(v):.1f}%"><span>{name}<b>{escape(labels[name])}</b></span></div>'
        for i, (name, v) in enumerate(pts)
    )
    zone = f'<div class="zone" style="left:{pos(item["floorPrice"]):.1f}%;width:{pos(item["askPrice"]) - pos(item["floorPrice"]):.1f}%"></div>'
    marker = ''
    if offer is not None:
        marker = f'<div class="offer" style="left:{pos(offer):.1f}%"><span>Brand offer<b>{escape(item["offerDisplay"] or "")}</b></span></div>'
    return f'<div class="bar" role="img" aria-label="Price range from walk-away to ask, with the brand offer marked">{zone}{ticks}{marker}</div>'


def html_report(item: dict) -> str:
    action = next_action(item['verdict'])
    tone = TONE[action]
    p = item['priceRange']
    who = escape(item.get('creatorName') or f"@{item['handle']}")
    rows = ''.join(
        f"<tr><td>{escape(li['item'])}</td><td class=\"num\">{escape(str(li['amount']))}</td>"
        f"<td class=\"src\">{'assumption' if li['isAssumption'] else escape(', '.join(li['sources']))}</td></tr>"
        for li in item['lineItems']
    )
    flags = ''
    if item.get('redFlags'):
        flags = '<section class="plain"><h2>Red flags</h2><ul class="flags">' + ''.join(
            f"<li><i>!</i><div><b>{escape(f['code'].replace('_', ' ').lower())}</b>{escape(f['message'])}</div></li>" for f in item['redFlags']
        ) + '</ul></section>'
    rs = (item.get('counterOptions') or {}).get('reducedScope')
    options = ''
    if rs:
        options = (
            '<section class="plain"><h2>Two options to offer</h2><div class="opts">'
            f"<div class=\"tile y\">{burst('mini', 10, 9)}<span>Full scope</span><b>{escape(p['ask'])}</b><small>everything the brand asked for</small></div>"
            f"<div class=\"tile l\">{sparkle('mini')}<span>Reduced scope</span><b>{escape(rs['price'])}</b><small>drops {escape(', '.join(_human(d) for d in rs['dropped']))}</small></div>"
            '</div></section>'
        )
    email = ''
    if item.get('counterEmail'):
        e = item['counterEmail']
        text = f"Subject: {e['subject']}\n\n{e['body']}"
        email = (
            '<section id="reply"><div class="head"><h2>Counter-offer email</h2>'
            '<button type="button" onclick="var t=document.getElementById(\'email\');t.select();'
            'navigator.clipboard&&navigator.clipboard.writeText(t.value);this.firstChild.textContent=\'Copied \'">Copy <span>&rarr;</span></button></div>'
            f'<textarea id="email" readonly rows="14">{escape(text)}</textarea>'
            + (f'<p class="note"><a href="{escape(item["counterEmailUrl"], quote=True)}">Open it as a designed email</a> to forward to the brand.</p>'
               if str(item.get('counterEmailUrl', '')).startswith('http') else '')
            + '</section>'
        )
    offer_pill = f'<span class="pill">Brand offer <b>{escape(item["offerDisplay"])}</b></span>' if item.get('offerDisplay') else ''
    tiles = (
        f'<div class="tiles">'
        f'<div class="tile p">{burst("mini", 8, 12, outline=True)}<span>Walk-away</span><b>{escape(p["walkAway"])}</b></div>'
        f'<div class="tile l">{sparkle("mini")}<span>Floor</span><b>{escape(p["floor"])}</b></div>'
        f'<div class="tile g">{squiggle("line")}<span>Fair</span><b>{escape(p["fair"])}</b></div>'
        f'<div class="tile b"><svg class="mini" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 18L18 6M9 6h9v9" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'
        f'<span>Ask</span><b>{escape(p["ask"])}</b></div></div>'
    )
    rates_html, numbers_html = _rate_card_html(item), _evidence_html(item)
    links = ([('verdict', 'Verdict')] + ([('rates', 'Rates')] if rates_html else []) + ([('reply', 'Reply')] if email else [])
             + ([('numbers', 'Numbers')] if numbers_html else []) + [('price', 'Price')] + ([] if rates_html else [('details', 'Details')]))
    price_title = 'Where the offer lands' if item.get('offerValue') is not None else 'Your package: price range'
    dock = ''.join(f'<a href="#{k}"{" class=\"on\"" if i == 0 else ""}>{t}</a>' for i, (k, t) in enumerate(links))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BVAL deal check</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<style>
:root{{--bg:#EEEEF0;--card:#fff;--card2:#F4F4F6;--ink:#0B0B0C;--muted:#5E5E66;--line:rgba(11,11,12,.09);--arc:#DCDCE1;
--glass:rgba(255,255,255,.55);--glass-edge:rgba(255,255,255,.85);--glass-in:rgba(255,255,255,.6);--blob:.55;--desk:#D6D6DC;
--lime:{LIME};--yellow:{YELLOW};--pink:{PINK};--blue:{BLUE};--lilac:{LILAC};--on:{INK_DARK};--tone:{tone}}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0B0B0C;--card:#17171A;--card2:#222226;--ink:#fff;--muted:#9A9AA2;--line:rgba(255,255,255,.08);--arc:#1C1C20;
--glass:rgba(30,30,34,.55);--glass-edge:rgba(255,255,255,.12);--glass-in:rgba(255,255,255,.06);--blob:.32;--desk:#000}}}}
*{{box-sizing:border-box}}
body{{margin:0;overflow-wrap:anywhere;background:var(--bg);color:var(--ink);font:15px/1.5 {BODY_FONT}}}
.arcs{{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;color:var(--arc)}}
.blobs{{position:absolute;inset:0;z-index:0;pointer-events:none;opacity:var(--blob);filter:blur(60px);
background:radial-gradient(28% 22% at 12% 18%,var(--lime),transparent 70%),radial-gradient(30% 24% at 92% 38%,var(--pink),transparent 70%),
radial-gradient(32% 26% at 8% 72%,var(--lilac),transparent 70%),radial-gradient(28% 22% at 88% 90%,var(--blue),transparent 70%)}}
main{{position:relative;z-index:1;padding:28px 16px 24px}}
.screen{{position:relative;min-height:100vh}}.content{{position:relative;overflow:hidden}}
.status{{display:none}}
.dock{{position:sticky;bottom:14px;z-index:5;display:flex;gap:2px;width:max-content;max-width:calc(100% - 24px);margin:0 auto 14px;padding:6px;border-radius:999px;
background:var(--glass);-webkit-backdrop-filter:blur(22px) saturate(170%);backdrop-filter:blur(22px) saturate(170%);border:1px solid var(--glass-edge);
box-shadow:0 12px 30px rgba(0,0,0,.15),inset 0 1px 0 var(--glass-edge)}}
.dock a{{color:var(--ink);text-decoration:none;font-size:13px;font-weight:500;padding:8px 14px;border-radius:999px;white-space:nowrap}}
.dock a.on{{background:var(--ink);color:var(--bg)}}
@media (min-width:600px){{
html{{background:var(--desk)}}body{{background:var(--desk);display:flex;justify-content:center;align-items:flex-start;padding:32px 0;min-height:100vh}}
.phone{{width:402px;height:min(874px,calc(100vh - 64px));padding:10px;border-radius:58px;background:#0E0E10;
box-shadow:0 40px 90px rgba(0,0,0,.35),inset 0 0 0 2px #2C2C31}}
.screen{{height:100%;min-height:0;border-radius:48px;overflow-y:auto;overflow-x:hidden;background:var(--bg);scrollbar-width:none}}
.screen::-webkit-scrollbar{{display:none}}
.status{{display:flex;position:sticky;top:0;z-index:6;justify-content:space-between;align-items:center;padding:12px 28px 8px;font-weight:700;font-size:15px;
background:var(--glass);-webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px)}}
.status .island{{width:112px;height:32px;border-radius:999px;background:#000}}.status svg{{display:block}}
main{{padding-top:16px}}}}
h1,h2,.label,.tile b,.opts b{{font-family:{DISPLAY_FONT};letter-spacing:-.01em}}
header{{position:relative;display:flex;align-items:center;gap:16px;padding-right:8px}}
header .who{{flex:1;min-width:0}}header p{{margin:0;color:var(--muted);font-size:13px}}
h1{{font-size:23px;line-height:1.15;margin:4px 0 0;font-weight:700}}
.avatar{{flex:none;border-radius:28px;box-shadow:0 10px 30px rgba(0,0,0,.18)}}
h2{{font-size:15px;font-weight:500;margin:0 0 12px}}
section{{border-radius:28px;padding:20px;margin-top:12px;background:var(--glass);-webkit-backdrop-filter:blur(22px) saturate(170%);
backdrop-filter:blur(22px) saturate(170%);border:1px solid var(--glass-edge);box-shadow:0 12px 40px rgba(0,0,0,.08),inset 0 1px 0 var(--glass-edge)}}
section.plain{{background:none;border:0;box-shadow:none;-webkit-backdrop-filter:none;backdrop-filter:none;padding:8px 0 0}}
.verdict,.tile,.flags li{{box-shadow:inset 0 1px 0 rgba(255,255,255,.55),inset 0 -12px 30px rgba(0,0,0,.05)}}
.verdict{{position:relative;overflow:hidden;background:var(--tone);color:var(--on);border-radius:28px;padding:24px 22px;margin-top:22px}}
.verdict .label{{display:block;font-size:22px;line-height:1.15;font-weight:700;max-width:78%}}
.verdict p{{margin:12px 0 0;position:relative;max-width:calc(100% - 64px)}}.verdict p.lead{{font-weight:700;font-size:15px}}
.verdict .burst{{position:absolute;right:-6px;top:-6px;width:92px;height:92px;color:var(--on)}}
.verdict .burst.ghost{{right:20px;top:auto;bottom:18px;width:40px;height:40px;opacity:.55}}
.pill{{display:inline-flex;gap:8px;align-items:center;margin-top:16px;color:var(--on);border-radius:999px;padding:6px 6px 6px 14px;font-size:13px;
background:rgba(255,255,255,.4);border:1px solid rgba(255,255,255,.7);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}}
.pill b{{font-family:{DISPLAY_FONT};font-weight:500;background:var(--on);color:#fff;border-radius:999px;padding:3px 10px}}
.tiles{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}}
.tile{{position:relative;overflow:hidden;border-radius:24px;padding:16px;min-height:112px;color:var(--on);display:flex;flex-direction:column;justify-content:flex-end}}
.tile span{{font-size:12px;font-weight:500;align-self:flex-start;margin-bottom:6px;background:rgba(255,255,255,.38);border:1px solid rgba(255,255,255,.6);
-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-radius:999px;padding:2px 10px}}.tile b{{font-size:20px;font-weight:700}}.tile small{{font-size:12px;opacity:.8}}
.tile .mini{{position:absolute;top:12px;right:12px;width:26px;height:26px}}
.tile .line{{position:absolute;top:14px;left:12px;right:12px;width:calc(100% - 24px);height:34px}}
.g{{background:var(--lime)}}.y{{background:var(--yellow)}}.p{{background:var(--pink)}}.b{{background:var(--blue)}}.l{{background:var(--lilac)}}
.bar{{position:relative;height:16px;border-radius:999px;background:var(--card2);margin:40px 10px 84px;box-shadow:inset 0 0 0 1.5px var(--line)}}
.bar{{background:var(--glass-in)}}
.zone{{position:absolute;top:0;bottom:0;background:var(--lime);border-radius:999px;box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}}
.tick,.offer{{position:absolute;top:-6px;width:2px;height:28px;margin-left:-1px;background:var(--muted)}}.tick.fair{{background:var(--ink)}}
.tick span,.offer span{{position:absolute;top:30px;left:50%;transform:translateX(-50%);font-size:11px;color:var(--muted);white-space:nowrap;text-align:center}}
.tick b,.offer b{{display:block;color:var(--ink);font-size:12px}}
.offer{{top:-7px;width:30px;height:30px;margin-left:-15px;border-radius:50%;background:var(--tone);border:4px solid var(--card);box-shadow:0 0 0 1.5px var(--ink)}}
.offer span{{top:-40px}}.tick.low span{{top:62px}}.tick.low::after{{content:"";position:absolute;left:0;top:28px;width:1px;height:32px;background:var(--line)}}
table{{width:100%;border-collapse:collapse}}td{{padding:10px 4px;overflow-wrap:normal;border-top:1px solid var(--line);vertical-align:top}}
tr:first-child td{{border-top:0}}
.num{{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;font-weight:700}}.src{{color:var(--muted);font-size:12px}}
.flags{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}
.flags li{{display:flex;gap:12px;align-items:flex-start;background:var(--pink);color:var(--on);border-radius:22px;padding:14px 16px}}
.flags i{{flex:none;width:26px;height:26px;border-radius:50%;background:var(--on);color:var(--pink);font:700 14px/26px {DISPLAY_FONT};text-align:center;font-style:normal}}
.flags b{{display:block;text-transform:capitalize;font-family:{DISPLAY_FONT};font-weight:500;font-size:14px}}
.opts{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.opts .tile{{min-height:140px}}.opts b{{font-size:24px}}
.head{{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px}}.head h2{{margin:0}}
button{{font:500 14px {BODY_FONT};padding:9px 10px 9px 18px;border-radius:999px;border:0;background:var(--ink);color:var(--bg);cursor:pointer;display:inline-flex;gap:8px;align-items:center}}
button span{{display:inline-block;width:24px;height:24px;line-height:24px;border-radius:50%;background:var(--lime);color:var(--on)}}
textarea{{width:100%;font:14px/1.55 {BODY_FONT};background:var(--glass-in);color:var(--ink);border:1px solid var(--glass-edge);border-radius:20px;padding:16px;resize:vertical}}
.ev{{list-style:none;margin:0;padding:0;display:grid;gap:10px}}.ev li{{border-top:1px solid var(--line);padding-top:10px}}.ev li:first-child{{border-top:0;padding-top:0}}
.ev-top{{display:flex;justify-content:space-between;gap:10px;align-items:baseline}}.ev-top span{{font-size:13px;color:var(--muted)}}.ev-top b{{font-family:{DISPLAY_FONT};font-size:15px;text-align:right}}
.ev small{{display:block;color:var(--muted);font-size:12px}}.ev p{{margin:4px 0 0;font-size:14px}}
.rc-packs{{grid-template-columns:1fr}}.rc-packs .tile{{min-height:0}}.note{{margin:10px 0 0;color:var(--muted);font-size:12px}}
footer{{display:flex;gap:8px;align-items:flex-start;color:var(--muted);font-size:12px;margin-top:22px}}
footer .sparkle{{flex:none;width:14px;height:14px;color:var(--lilac);margin-top:2px}}
</style></head><body>
<div class="phone"><div class="screen">
<div class="status" aria-hidden="true"><span>9:41</span><span class="island"></span>
<svg width="66" height="14" viewBox="0 0 66 14"><g fill="currentColor"><rect x="0" y="9" width="3" height="5" rx="1"/><rect x="5" y="6" width="3" height="8" rx="1"/>
<rect x="10" y="3" width="3" height="11" rx="1"/><rect x="15" y="0" width="3" height="14" rx="1"/>
<path d="M30 4a9 9 0 0 1 12 0l-1.6 1.7a6.6 6.6 0 0 0-8.8 0zM32.6 7a5.4 5.4 0 0 1 6.8 0L36 10.6z"/>
<rect x="44" y="1.5" width="19" height="11" rx="3.5" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".5"/><rect x="46" y="3.5" width="13" height="7" rx="2"/>
<rect x="64" y="5" width="1.6" height="4" rx=".8" opacity=".5"/></g></svg></div>
<div class="content">
<div class="blobs" aria-hidden="true"></div>
<svg class="arcs" viewBox="0 0 400 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.5">
<circle cx="-40" cy="620" r="260"/><circle cx="460" cy="120" r="210"/></g></svg>
<main>
<header>{avatar_svg(item['handle'])}
<div class="who"><p>BVAL deal check · {escape(item['platform'].title())} · {escape(item['marketName'])}</p><h1>{who}</h1></div></header>
<div class="verdict" id="verdict">{burst()}{burst('burst ghost', 8, 10, outline=True)}<span class="label">{escape(VERDICT_LABEL.get(item['verdict'], item['verdict']))}</span>
<p class="lead">{escape(summary_line(item))}</p><p>{escape(item['verdictText'])}</p>{offer_pill}</div>
{tiles}
{rates_html}
{email}
{numbers_html}
<section id="price"><h2>{price_title}</h2>{_range_bar(item)}</section>
{options}{flags}
<section id="details"><h2>Line items</h2><table>{rows}</table></section>
<section><h2>Data used</h2><p style="margin:0">{escape(_data_used(item))}</p></section>
<footer>{sparkle()}<span>{escape(item['disclaimer'])} Rates version {escape(str(item['ratesVersion']))}. Evaluated {escape(item['evaluatedAt'])}.</span></footer>
</main></div>
<nav class="dock" aria-label="Sections">{dock}</nav>
</div></div>
<script>document.querySelectorAll('.dock a').forEach(function(a){{a.onclick=function(){{
document.querySelectorAll('.dock a').forEach(function(b){{b.classList.remove('on')}});a.classList.add('on')}}}})</script>
</body></html>"""


def _initial(item: dict) -> str:
    for ch in (item.get('creatorName') or '') + item['handle']:
        if ch.isalnum():
            return ch.upper()
    return 'B'


def email_digest(item: dict) -> tuple[str, str, str]:
    """Subject, HTML and plain-text bodies for emailing the result to the user.

    Mail clients strip positioning, SVG and most <style> rules, so this uses inline styles and tables only.
    The drawn figures become text glyphs (✦ ✳ ↗), the avatar becomes an initial on a colour tile, and the
    price bar is left to the full HTML report linked at the bottom.
    """
    action = next_action(item['verdict'])
    tone = TONE[action]
    p = item['priceRange']
    label = VERDICT_LABEL.get(item['verdict'], item['verdict'])
    offer = f", offer {item['offerDisplay']}" if item.get('offerDisplay') else ''
    subject = f"BVAL: {label} for @{item['handle']}{offer} (fair {p['fair']})"
    avatar_bg = [LIME, YELLOW, PINK, BLUE, LILAC][hashlib.sha256(item['handle'].lower().encode()).digest()[0] % 5]
    disp = f"font-family:{DISPLAY_FONT}"
    offer_chip = (f'<div style="margin-top:16px"><span style="display:inline-block;border-radius:999px;padding:5px 5px 5px 14px;font-size:13px;{GLASS_CHIP}">'
                  f'Brand offer <b style="display:inline-block;margin-left:6px;background:{INK_DARK};color:#ffffff;border-radius:999px;padding:3px 10px">'
                  f'{escape(item["offerDisplay"])}</b></span></div>') if item.get('offerDisplay') else ''

    def tile(bg: str, fg: str, glyph: str, name: str, value: str, note: str = '') -> str:
        note_html = f'<div style="font-size:12px;opacity:.75;margin-top:2px">{note}</div>' if note else ''
        dark = fg == '#ffffff'
        box = (f'background:#18181B;background:{GLASS_DARK};border:1px solid {GLASS_DARK_EDGE}' if dark
               else f'background:{bg};border:1px solid rgba(255,255,255,.55)')
        chip = GLASS_CHIP_DARK if dark else GLASS_CHIP
        return (f'<div style="{box};color:{fg};border-radius:22px;padding:16px 18px">'
                f'<div style="font-size:18px;line-height:1;text-align:right;height:18px">{glyph}</div>'
                f'<span style="display:inline-block;margin-top:8px;font-size:12px;font-weight:500;border-radius:999px;padding:2px 10px;{chip}">{name}</span>'
                f'<div style="{disp};font-size:22px;font-weight:700;line-height:1.2">{escape(value)}</div>{note_html}</div>')

    tiles = (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px"><tr>'
        f'<td width="50%" style="padding:0 5px 10px 0;vertical-align:top">{tile("", "#ffffff", "✦", "Brand offer", item.get("offerDisplay") or "-", "what they proposed")}</td>'
        f'<td width="50%" style="padding:0 0 10px 5px;vertical-align:top">{tile(LIME, INK_DARK, "〰", "Fair", p["fair"], "floor " + escape(p["floor"]))}</td>'
        '</tr><tr>'
        f'<td width="50%" style="padding:0 5px 0 0;vertical-align:top">{tile(BLUE, INK_DARK, "↗", "Ask", p["ask"], "open with this")}</td>'
        f'<td width="50%" style="padding:0 0 0 5px;vertical-align:top">{tile(PINK, INK_DARK, "✳", "Walk-away", p["walkAway"], "below this, say no")}</td>'
        '</tr></table>'
    )
    counter = ''
    if item.get('counterEmail'):
        e = item['counterEmail']
        counter = (
            f'<div style="background:#18181B;background:{GLASS_DARK};border:1px solid {GLASS_DARK_EDGE};border-radius:26px;padding:20px;margin-top:12px">'
            f'<div style="{disp};font-size:15px;font-weight:500;color:#ffffff">Your counter-offer email '
            f'<span style="display:inline-block;margin-left:6px;background:{LIME};color:{INK_DARK};border-radius:999px;padding:2px 10px;font-size:11px;font-family:{BODY_FONT};font-weight:700">ready to copy</span></div>'
            '<div style="margin-top:12px;background:#222226;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:16px;white-space:pre-wrap;font-size:14px;line-height:1.55;color:#E8E8EA">'
            f"<b style=\"color:#ffffff\">Subject:</b> {escape(e['subject'])}\n\n{escape(e['body'])}</div></div>"
        )
    flags = ''
    if item.get('redFlags'):
        flags = (f'<div style="{disp};font-size:15px;font-weight:500;color:#ffffff;margin:22px 0 10px">Red flags</div>' + ''.join(
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:8px"><tr>'
            f'<td style="background:{PINK};color:{INK_DARK};border-radius:20px;padding:14px 16px;font-size:14px">'
            f'<span style="display:inline-block;width:22px;height:22px;line-height:22px;border-radius:50%;background:{INK_DARK};color:{PINK};text-align:center;font-weight:700;margin-right:8px">!</span>'
            f"{escape(f['message'])}</td></tr></table>"
            for f in item['redFlags']
        ))
    link = ''
    if item.get('reportUrl', '').startswith('http'):
        link = (f'<p style="margin:26px 0 0"><a href="{escape(item["reportUrl"], quote=True)}" '
                f'style="display:inline-block;background:#ffffff;color:{INK_DARK};padding:14px 14px 14px 24px;border-radius:999px;text-decoration:none;font-weight:700;font-size:15px">'
                f'Open the full report&nbsp;&nbsp;<span style="display:inline-block;width:28px;height:28px;line-height:28px;text-align:center;border-radius:50%;background:{LIME};color:{INK_DARK}">&rarr;</span></a></p>')
    rc_packs = (item.get('rateCard') or {}).get('packages') or []
    packs = ''
    if rc_packs:
        cols = [LIME, YELLOW, LILAC]
        packs = (f'<div style="{disp};font-size:15px;font-weight:500;color:#ffffff;margin:22px 0 10px">What to charge: ready-made packages</div>' + ''.join(
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:8px"><tr>'
            f'<td style="background:{cols[i % 3]};color:{INK_DARK};border-radius:20px;padding:14px 16px;font-size:13px">'
            f'<div style="font-size:12px;font-weight:500">{escape(pk["name"])}</div>'
            f'<div style="{disp};font-size:20px;font-weight:700">{escape(pk["ask"])}</div>'
            f'<div style="opacity:.8">fair {escape(pk["fair"])} · {escape(", ".join(pk["includes"]))}</div></td></tr></table>'
            for i, pk in enumerate(rc_packs)))
    html = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark"><meta name="supported-color-schemes" content="dark"><link rel="stylesheet" href="{FONTS}"></head>
<body style="margin:0;padding:0;background:{INK_DARK}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="{INK_DARK}" style="background:{INK_DARK}"><tr><td align="center" style="padding:24px 10px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:440px;font-family:{BODY_FONT};font-size:15px;line-height:1.5;color:#ffffff;
background-color:#0F0F11;background-image:radial-gradient(60% 30% at 0% 0%,rgba(59,227,107,.22),transparent),radial-gradient(60% 30% at 100% 55%,rgba(242,108,181,.18),transparent),radial-gradient(70% 30% at 0% 100%,rgba(166,140,247,.22),transparent);
border:1px solid rgba(255,255,255,.12);border-radius:40px">
<tr><td style="padding:26px 18px 0">
<table role="presentation" cellpadding="0" cellspacing="0"><tr>
<td style="width:56px;height:56px;border-radius:18px;background:{avatar_bg};color:{INK_DARK};text-align:center;vertical-align:middle;{disp};font-size:24px;font-weight:700">{escape(_initial(item))}</td>
<td style="padding-left:14px"><div style="color:#8D8D94;font-size:13px">BVAL deal check · {escape(item['platform'].title())}</div>
<div style="{disp};font-size:22px;font-weight:700;color:#ffffff">@{escape(item['handle'])}</div></td></tr></table>
</td></tr>
<tr><td style="padding:20px 18px 28px">
<div style="background:{tone};border:1px solid rgba(255,255,255,.55);color:{INK_DARK};border-radius:28px;padding:24px 22px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td style="{disp};font-size:24px;font-weight:700;line-height:1.2;color:{INK_DARK}">{escape(label)}</td>
<td width="44" style="font-size:40px;line-height:1;text-align:right;vertical-align:top;color:{INK_DARK}">✳</td></tr></table>
<div style="margin-top:12px;font-weight:700;font-size:16px">{escape(summary_line(item))}</div>
{offer_chip}</div>
{tiles}{packs}{counter}{flags}{link}
<p style="color:#8D8D94;font-size:12px;margin:28px 0 0">✦ {escape(item['disclaimer'])}</p>
</td></tr></table>
</td></tr></table></body></html>"""

    text_parts = [f'{label}: {summary_line(item)}', '',
                  f"Brand offer {item.get('offerDisplay') or '-'} | walk-away {p['walkAway']} | floor {p['floor']} | fair {p['fair']} | ask {p['ask']}"]
    if item.get('counterEmail'):
        text_parts += ['', 'Your counter-offer email:', '', f"Subject: {item['counterEmail']['subject']}", '', item['counterEmail']['body']]
    if link:
        text_parts += ['', f"Full report: {item['reportUrl']}"]
    text_parts += ['', item['disclaimer']]
    return subject, html, '\n'.join(text_parts)


def agent_fields(item: dict) -> dict[str, Any]:
    return {'nextAction': next_action(item['verdict']), 'summary': summary_line(item)}


def counter_email_html(item: dict) -> tuple[str, str, str] | None:
    """The counter-offer email to the brand, laid out in the report's visual style, ready to forward.

    Brand-facing, so it carries no BVAL branding (the email must never reveal that a tool produced the numbers).
    Built from the drafted text: '- label: amount' lines become a quote card, other '- ' lines a list,
    everything else paragraphs. Every value is escaped.
    """
    e = item.get('counterEmail')
    if not e:
        return None
    disp = f"font-family:{DISPLAY_FONT}"
    avatar_bg = [LIME, YELLOW, PINK, BLUE, LILAC][hashlib.sha256(item['handle'].lower().encode()).digest()[0] % 5]
    sender = item.get('creatorName') or f"@{item['handle']}"

    def para(text: str) -> str:
        return f'<p style="margin:0 0 14px;color:#E8E8EA">{escape(text)}</p>'

    def quote_card(rows: list[tuple[str, str]]) -> str:
        cells = ''.join(
            f'<tr><td style="padding:9px 0;border-top:1px solid rgba(11,11,12,.12);font-size:14px">{escape(k)}</td>'
            f'<td style="padding:9px 0 9px 12px;border-top:1px solid rgba(11,11,12,.12);text-align:right;white-space:nowrap;{disp};font-weight:700">{escape(v)}</td></tr>'
            for k, v in rows
        )
        return (f'<div style="background:{LIME};color:{INK_DARK};border-radius:22px;padding:16px 18px;margin:0 0 14px">'
                f'<div style="font-size:12px;font-weight:500;margin-bottom:4px">Itemised quote</div>'
                f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="color:{INK_DARK}">{cells}</table></div>')

    def bullets(items: list[str]) -> str:
        lis = ''.join(f'<li style="margin:0 0 6px">{escape(t)}</li>' for t in items)
        return (f'<div style="background:#18181B;background:{GLASS_DARK};border:1px solid {GLASS_DARK_EDGE};border-radius:22px;padding:14px 18px 8px;margin:0 0 14px">'
                f'<ul style="margin:0;padding-left:18px;color:#E8E8EA;font-size:14px">{lis}</ul></div>')

    parts: list[str] = []
    for block in e['body'].strip().split('\n\n'):
        text_lines: list[str] = []
        dash: list[str] = []

        def flush_dash() -> None:
            if not dash:
                return
            priced = [ln.split(': ', 1) for ln in dash]
            if all(len(x) == 2 and any(ch.isdigit() for ch in x[1]) for x in priced):
                parts.append(quote_card([(k, v) for k, v in priced]))
            else:
                parts.append(bullets(dash))
            dash.clear()

        for line in block.split('\n'):
            if line.lstrip().startswith('- '):
                if text_lines:
                    parts.append(para(' '.join(text_lines)))
                    text_lines.clear()
                dash.append(line.lstrip()[2:].strip())
            else:
                flush_dash()
                text_lines.append(line.strip())
        flush_dash()
        if text_lines:
            parts.append(para('\n'.join(text_lines)).replace('\n', '<br>'))

    html = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark"><meta name="supported-color-schemes" content="dark"><link rel="stylesheet" href="{FONTS}"></head>
<body style="margin:0;padding:0;background:{INK_DARK}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="{INK_DARK}" style="background:{INK_DARK}"><tr><td align="center" style="padding:24px 10px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;font-family:{BODY_FONT};font-size:15px;line-height:1.55;color:#ffffff;
background-color:#0F0F11;background-image:radial-gradient(60% 30% at 0% 0%,rgba(59,227,107,.18),transparent),radial-gradient(70% 30% at 100% 100%,rgba(166,140,247,.2),transparent);
border:1px solid rgba(255,255,255,.12);border-radius:36px">
<tr><td style="padding:26px 22px 0">
<table role="presentation" cellpadding="0" cellspacing="0"><tr>
<td style="width:52px;height:52px;border-radius:17px;background:{avatar_bg};color:{INK_DARK};text-align:center;vertical-align:middle;{disp};font-size:22px;font-weight:700">{escape(_initial(item))}</td>
<td style="padding-left:14px"><div style="color:#8D8D94;font-size:13px">Partnership proposal</div>
<div style="{disp};font-size:19px;font-weight:700;color:#ffffff">{escape(e['subject'])}</div></td></tr></table>
</td></tr>
<tr><td style="padding:22px 22px 12px">{''.join(parts)}</td></tr>
<tr><td style="padding:0 22px 24px;color:#8D8D94;font-size:12px">{escape(sender)} · {escape(item['platform'].title())}</td></tr>
</table></td></tr></table></body></html>"""
    return e['subject'], html, f"Subject: {e['subject']}\n\n{e['body']}"
