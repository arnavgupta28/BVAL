"""Render the README graphics in the BVAL visual style (see assets/design) to PNG with headless Chrome.

READMEs on GitHub and Apify Store strip CSS, so the style ships as images. The avatars, starbursts and the
report/email previews reuse bval/my_actor/report.py, so the README always matches what the Actor outputs.

Run from the repo root:  python3 assets/readme/build_readme_images.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'bval'))

from my_actor.report import (  # noqa: E402
    BLUE, DISPLAY_FONT, BODY_FONT, FONTS, INK_DARK, LILAC, LIME, PINK, YELLOW,
    avatar_svg, burst, email_digest, html_report, sparkle, squiggle,
)

CHROME_FRAME = 87  # headless Chrome's viewport is this much shorter than --window-size
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
DISPLAY = DISPLAY_FONT.replace("'Unbounded',", "'Unbounded','Avenir Next',")

DEMO = {
    'handle': 'priya.fit', 'platform': 'instagram', 'creatorName': 'Priya', 'marketName': 'Global (US benchmarks)',
    'verdict': 'DECLINE_OR_REDUCE_SCOPE',
    'verdictText': 'The offer is below your walk-away price. Send the counter: full scope at your ask, or a lighter version near their budget.',
    'offerDisplay': '$800', 'offerValue': 800, 'gapPct': 71.3,
    'walkAwayPrice': 910, 'floorPrice': 2370, 'fairPrice': 2790, 'askPrice': 3490,
    'priceRange': {'walkAway': '$910', 'floor': '$2,370', 'fair': '$2,790', 'ask': '$3,490'},
    'lineItems': [
        {'item': '1 x Instagram Reel', 'amount': '$990', 'sources': ['Later', 'Influencer Marketing Hub'], 'isAssumption': False},
        {'item': 'Organic usage rights, 90 days', 'amount': '$160', 'sources': ['Lumanu'], 'isAssumption': False},
        {'item': 'Meta Partnership Ads, 30 days', 'amount': '$280', 'sources': ['impact.com'], 'isAssumption': False},
        {'item': 'Category exclusivity (fitness), 180 days', 'amount': '$1,360', 'sources': ['Toptal', 'Modash'], 'isAssumption': False},
    ],
    'counterOptions': {'reducedScope': {'price': '$1,070', 'dropped': ['exclusivity', 'whitelisting', 'organic_usage']}},
    'redFlags': [
        {'code': 'UNPRICED_WHITELISTING', 'message': 'Ads through your handle are asked for but not paid for: worth $280.'},
        {'code': 'LONG_EXCLUSIVITY', 'message': 'Exclusivity beyond 7 days is worth +$1,364 on its own.'},
    ],
    'metrics': {'audience': 85000, 'tier': 'micro', 'medianViews': 42000, 'engagementRate': 0.035, 'postsUsed': 24},
    'confidence': 'medium', 'confidenceReasons': [],
    'counterEmail': {
        'subject': 'Re: Acme Protein x Priya',
        'body': ("Hi Acme Protein team,\n\nThanks for thinking of me, I'd love to make this work. Based on my recent Reels "
                 "(42K median plays) the full package, with 90 days of usage, 30 days of Partnership Ads and 6 months of "
                 "fitness exclusivity, comes to $3,490.\n\nIf that's above budget, I can do the Reel with 30 days of usage "
                 "and no exclusivity for $1,070.\n\nHappy to jump on a call.\nPriya"),
    },
    'disclaimer': 'Benchmark-based estimate, not financial or legal advice.',
    'ratesVersion': '2026-11', 'evaluatedAt': '2026-11-22T10:30:00+00:00',
    'reportUrl': 'https://api.apify.com/v2/key-value-stores/demo/records/QUOTE.html',
}

BASE_CSS = f"""
*{{box-sizing:border-box}}html,body{{margin:0;overflow:hidden}}
body{{background:{INK_DARK};color:#fff;font:16px/1.45 {BODY_FONT}}}
.d{{font-family:{DISPLAY};letter-spacing:-.015em}}
.stage{{position:relative;overflow:hidden}}
.arcs{{position:absolute;inset:0;width:100%;height:100%;color:#1C1C20}}
.card{{position:relative;overflow:hidden;border-radius:30px;padding:26px;color:{INK_DARK}}}
.pill{{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:8px 16px;font-size:14px;font-weight:500}}
.num{{font:700 14px/1 {DISPLAY};display:inline-flex;width:38px;height:38px;border-radius:50%;background:{INK_DARK};color:#fff;align-items:center;justify-content:center}}
svg.burst,svg.sparkle,svg.squiggle{{display:block}}
"""

ARCS = ('<svg class="arcs" viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
        '<g fill="none" stroke="currentColor" stroke-width="2"><circle cx="-60" cy="640" r="420"/><circle cx="1260" cy="-40" r="360"/></g></svg>')


def page(body: str, w: int, h: int) -> str:
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
            f'<style>{BASE_CSS}</style></head><body><div class="stage" style="width:{w}px;height:{h}px">{ARCS}{body}</div></body></html>')


def neon(w: int = 180) -> str:
    return (f'<svg width="{w}" height="{w * 56 // 120}" viewBox="0 0 120 56" aria-hidden="true"><defs><linearGradient id="ng" x1="0" x2="1">'
            f'<stop offset="0" stop-color="{LIME}"/><stop offset=".5" stop-color="{PINK}"/><stop offset="1" stop-color="{LILAC}"/></linearGradient></defs>'
            '<path d="M2 50H40L78 8H118" fill="none" stroke="url(#ng)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


SHOT_W, SHOT_H = 500, 1087  # 402:874, an iPhone screen; headless Chrome's narrowest window is 500px


def phone(img: Path, w: int, screen_bg: str, offset: float = 0, light_text: bool = False) -> str:
    """A phone in the style of the design references: black bezel, dynamic island, status bar, glass edge."""
    r, pad, bar = w * 0.145, w * 0.026, w * 0.11
    ink = '#ffffff' if light_text else INK_DARK
    return (f'<div style="width:{w}px;height:{w * 874 / 402:.0f}px;border-radius:{r:.0f}px;padding:{pad:.0f}px;background:#0E0E10;'
            f'box-shadow:0 40px 80px rgba(0,0,0,.55),inset 0 0 0 2px #2C2C31,inset 0 0 0 {pad - 2:.0f}px #0E0E10">'
            f'<div style="position:relative;width:100%;height:100%;border-radius:{r - pad:.0f}px;overflow:hidden;background:{screen_bg}">'
            f'<div style="position:absolute;z-index:2;top:0;left:0;right:0;height:{bar:.0f}px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:0 {w * 0.08:.0f}px;font:700 {w * 0.04:.0f}px {BODY_FONT};color:{ink};background:{screen_bg}">'
            f'<span>9:41</span><span style="width:{w * 0.28:.0f}px;height:{w * 0.08:.0f}px;border-radius:999px;background:#000"></span>'
            f'<span style="letter-spacing:2px">▮▮▮</span></div>'
            f'<img src="{img.as_uri()}" style="position:absolute;top:{bar:.0f}px;left:0;width:100%;margin-top:-{offset * (w - 2 * pad):.0f}px"></div></div>')


def banner(shots: dict[str, Path]) -> tuple[str, int, int]:
    w, h = 1200, 520
    body = f"""
<div style="position:absolute;left:-150px;bottom:-250px;width:420px;height:420px;color:{PINK};opacity:.9">{burst('burst', 8, 10)}</div>
<div style="position:absolute;left:560px;bottom:-150px;width:240px;height:240px;color:#fff;opacity:.3">{burst('burst', 8, 9, outline=True)}</div>
<div style="position:absolute;right:40px;top:26px">{neon(170)}</div>
<div style="position:absolute;left:64px;top:56px;width:640px">
  <div style="display:flex;align-items:center;gap:10px"><span style="width:26px;height:26px;color:{LIME}">{sparkle()}</span>
  <span class="d" style="font-size:26px;font-weight:700">BVAL</span>
  <span class="pill" style="background:#1C1C20;color:#B9B9C0;margin-left:8px">Apify Actor · Instagram · TikTok · YouTube</span></div>
  <div class="d" style="font-size:64px;line-height:1.02;font-weight:700;margin-top:34px">Know your<br><span style="color:{LIME}">worth</span> before<br>you reply.</div>
  <div style="font-size:19px;color:#B9B9C0;margin-top:20px;max-width:520px">Paste a brand's offer. Get the verdict, your price range, every term priced, and a counter-offer email.</div>
</div>
<div style="position:absolute;right:120px;top:70px;width:300px;height:300px;border-radius:50%;background:{LILAC};filter:blur(70px);opacity:.55"></div>
<div style="position:absolute;right:150px;top:84px;transform:rotate(6deg)">{phone(shots['report'], 250, '#EEEEF0')}</div>
<div style="position:absolute;right:390px;top:150px;transform:rotate(-10deg)">{avatar_svg('zahra.cooks', 104)}</div>
<div style="position:absolute;right:40px;top:120px;transform:rotate(9deg)">{avatar_svg('kai.travel', 112)}</div>
<div style="position:absolute;right:56px;top:300px;padding:12px 16px;border-radius:22px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.28);
  -webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);font-size:13px;color:#fff;box-shadow:0 20px 40px rgba(0,0,0,.35)">
  Brand offered <b>$800</b><div class="d" style="font-size:20px;font-weight:700;color:{LIME}">Counter $3,490</div></div>"""
    return page(body, w, h), w, h


def how() -> tuple[str, int, int]:
    w, h = 1200, 380
    steps = [
        (LIME, '01', 'Scrape real views', "Apify's own scrapers read median Reel, TikTok and YouTube views. Not followers.", squiggle('squiggle')),
        (YELLOW, '02', 'Price every term', 'Usage, Partnership / Spark Ads, exclusivity, rush: each a cited line item.', sparkle()),
        (PINK, '03', 'Give the verdict', 'Accept, counter, trade scope or decline, with walk-away / floor / fair / ask.', burst('burst', 10, 8)),
        (BLUE, '04', 'Draft the counter', 'A ready-to-send email with two options: full scope, or a lighter version.',
         '<svg viewBox="0 0 24 24"><path d="M5 19L19 5M9 5h10v10" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>'),
    ]
    cards = ''.join(
        f'<div class="card" style="background:{c};flex:1;display:flex;flex-direction:column;justify-content:space-between">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start"><span class="num">{n}</span>'
        f'<span style="width:{90 if n == "01" else 46}px;height:46px">{fig}</span></div>'
        f'<div><div class="d" style="font-size:22px;font-weight:700;line-height:1.15">{t}</div>'
        f'<div style="font-size:15px;margin-top:8px">{d}</div></div></div>'
        for c, n, t, d, fig in steps
    )
    body = (f'<div style="position:absolute;inset:36px 40px"><div class="d" style="font-size:24px;font-weight:500;margin-bottom:18px">How it works</div>'
            f'<div style="display:flex;gap:14px;height:270px">{cards}</div></div>')
    return page(body, w, h), w, h


def who() -> tuple[str, int, int]:
    w, h = 1200, 330
    people = [
        (LILAC, 'mia.makes', 'Creators', '10K to 1M followers, getting offers with usage, ads and exclusivity clauses.'),
        (YELLOW, 'dev.talent', 'Talent managers', 'Triage dozens of inbound offers a week across a roster, via API or an AI agent.'),
        (LIME, 'acme.brand', 'Brands', 'Offer fair deals up front and close faster.'),
    ]
    cards = ''.join(
        f'<div class="card" style="background:{c};flex:1;display:flex;gap:20px;align-items:center">'
        f'<div style="flex:none">{avatar_svg(seed, 104)}</div>'
        f'<div><div class="d" style="font-size:22px;font-weight:700">{t}</div><div style="font-size:15px;margin-top:6px">{d}</div></div></div>'
        for c, seed, t, d in people
    )
    body = (f'<div style="position:absolute;inset:36px 40px"><div class="d" style="font-size:24px;font-weight:500;margin-bottom:18px">Who it\'s for</div>'
            f'<div style="display:flex;gap:14px;height:200px">{cards}</div></div>')
    return page(body, w, h), w, h


def verdicts() -> tuple[str, int, int]:
    w, h = 1200, 200
    items = [(LIME, 'Accept', 'nextAction: accept'), (YELLOW, 'Counter', 'nextAction: counter'),
             (PINK, 'Decline or cut scope', 'nextAction: decline'), (BLUE, 'Your quote', 'nextAction: quote')]
    cards = ''.join(
        f'<div class="card" style="background:{c};flex:1;padding:22px 24px"><div style="position:absolute;right:16px;top:16px;width:34px;height:34px">{burst("burst", 10, 8)}</div>'
        f'<div class="d" style="font-size:21px;font-weight:700;max-width:80%">{t}</div>'
        f'<div style="font:500 13px ui-monospace,Menlo,monospace;margin-top:10px">{s}</div></div>'
        for c, t, s in items
    )
    return page(f'<div style="position:absolute;inset:32px 40px;display:flex;gap:14px">{cards}</div>', w, h), w, h


def pricing() -> tuple[str, int, int]:
    w, h = 1200, 330
    tiles = [(LIME, 'Deal evaluated', 'scrape + pricing + verdict', '$0.79'),
             (PINK, 'Counter email drafted', 'written from the numbers', '$0.20'),
             (BLUE, 'Re-priced, no scrape', 'with manual metrics', '$0.25')]
    small = ''.join(
        f'<div class="card" style="background:{c};flex:1;display:flex;flex-direction:column;justify-content:flex-end">'
        f'<div style="font-size:15px;font-weight:700">{t}</div><div style="font-size:13px;opacity:.8">{s}</div>'
        f'<div class="d" style="font-size:36px;font-weight:700;margin-top:8px">{p}</div></div>'
        for c, t, s, p in tiles
    )
    body = f"""<div style="position:absolute;inset:36px 40px">
<div class="d" style="font-size:24px;font-weight:500;margin-bottom:18px">Pay per event</div>
<div style="display:flex;gap:14px;height:220px">
<div class="card" style="background:{YELLOW};flex:1.3;display:flex;flex-direction:column;justify-content:space-between">
  <div style="position:absolute;right:-10px;top:-10px;width:110px;height:110px">{burst()}</div>
  <span class="pill" style="background:{INK_DARK};color:#fff;align-self:flex-start">Full deal check</span>
  <div><div class="d" style="font-size:64px;font-weight:700;line-height:1">$0.99</div>
  <div style="font-size:15px;margin-top:8px">One better-negotiated deal pays for a year of checks.</div></div></div>
{small}</div></div>"""
    return page(body, w, h), w, h


def output(shots: dict[str, Path]) -> tuple[str, int, int]:
    w, h = 1200, 900

    def col(img: Path, label: str, color: str, bg: str, offset: float = 0, light: bool = False) -> str:
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:18px">'
                f'<span class="pill" style="background:{color};color:{INK_DARK}">{label}</span>{phone(img, 320, bg, offset, light)}</div>')

    body = f"""<div style="position:absolute;left:180px;top:260px;width:340px;height:340px;border-radius:50%;background:{LIME};filter:blur(90px);opacity:.35"></div>
<div style="position:absolute;right:160px;top:200px;width:340px;height:340px;border-radius:50%;background:{PINK};filter:blur(90px);opacity:.35"></div>
<div style="position:absolute;right:-40px;top:-40px;width:200px;height:200px;color:{LILAC};opacity:.9">{burst('burst', 8, 10)}</div>
<div style="position:absolute;inset:36px 40px;display:flex;flex-direction:column">
<div class="d" style="font-size:24px;font-weight:500;margin-bottom:22px">What you get</div>
<div style="display:flex;justify-content:space-between">
{col(shots['report'], 'Deal report · Output tab', LIME, '#EEEEF0')}
{col(shots['email'], 'In your inbox', PINK, INK_DARK, 0.02, True)}
{col(shots['report_dark'], 'Price, options, red flags', YELLOW, INK_DARK, 1.75, True)}
</div></div>"""
    return page(body, w, h), w, h


def shoot(html: str, w: int, h: int, out: Path, tmp: Path, dark: bool = False) -> None:
    src = tmp / f'{out.stem}.html'
    # Headless Chrome's viewport is CHROME_FRAME px shorter than the window and sips only crops from the centre,
    # so pad the page by CHROME_FRAME on top, grow the window by twice that, and centre-crop back to w x h.
    src.write_text(html.replace('</head>', f'<style>body{{padding-top:{CHROME_FRAME}px!important}}</style></head>', 1))
    args = [CHROME, '--headless', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
            '--virtual-time-budget=8000', f'--window-size={w},{h + 2 * CHROME_FRAME}', f'--screenshot={out}', src.as_uri()]
    if dark:
        args.insert(2, '--force-dark-mode')
        args.insert(2, '--blink-settings=preferredColorScheme=0')
    subprocess.run(args, check=True, capture_output=True)
    subprocess.run(['sips', '-c', str(h * 2), str(w * 2), str(out)], check=True, capture_output=True)
    if out.is_relative_to(ROOT):
        print('wrote', out.relative_to(ROOT))


def main() -> None:
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        shots = {'report': tmp / 'shot_report.png', 'email': tmp / 'shot_email.png', 'report_dark': tmp / 'shot_report_dark.png'}
        report = html_report(DEMO)
        shoot(report, SHOT_W, SHOT_H, shots['report'], tmp)
        shoot(report, SHOT_W, SHOT_H * 3, shots['report_dark'], tmp, dark=True)
        shoot(email_digest(DEMO)[1], SHOT_W, SHOT_H, shots['email'], tmp)
        shoot(*banner(shots), OUT / 'banner.png', tmp)
        for name, build in (('how', how), ('who', who), ('verdicts', verdicts), ('pricing', pricing)):
            shoot(*build(), OUT / f'{name}.png', tmp)
        shoot(*output(shots), OUT / 'output.png', tmp)


if __name__ == '__main__':
    main()
