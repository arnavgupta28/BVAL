**Paste a brand's offer. Get the verdict, your walk-away / floor / fair / ask price, every term priced as its own line, and a counter-offer email ready to send.** For creators and talent managers on **Instagram, TikTok and YouTube**, in **any country**.

> *"Acme Protein offered Priya $800 for one Reel, 90 days of usage, 30 days of ads through her handle and 6 months of category exclusivity. BVAL says: fair value $2,790, walk-away $910. The exclusivity alone is worth $1,360. Counter at $3,490, or offer a lighter version at $1,070."*

## What does BVAL do?

BVAL is a **brand-deal valuation API** for the creator economy. Give it a creator's **handle** and the brand's **deal terms**. It:

1. **Scrapes real recent performance** with Apify's own Instagram, TikTok and YouTube scrapers (median Reel plays, TikTok plays, YouTube views on videos 30+ days old), not follower counts.
2. **Prices every term** from a cited 2026 benchmark table: the content, organic and paid usage rights, **Meta Partnership Ads / TikTok Spark Ads** (whitelisting), exclusivity, rush, revisions, raw footage, link placements and bundles.
3. **Gives a verdict** on the brand's offer (accept, counter, trade scope, or decline) with a **walk-away / floor / fair / ask** range and **red flags** such as perpetual rights, free exclusivity or unpaid whitelisting.
4. **Drafts the counter-offer email** using only the computed numbers, with a two-option close: full scope at your ask, or a reduced scope near their budget.

The price is never made up by an AI. It comes from a transparent formula and a versioned `rates.json` where every number cites a source or is labelled as an assumption. The LLM only writes the email.

## Who is it for?

- 🎥 **Creators (10K–1M followers)** who get offers with usage, whitelisting and exclusivity clauses and don't know what those are worth.
- 🧑‍💼 **Talent managers and influencer agencies** triaging dozens of inbound offers a week across a roster, via API, schedules or AI agents (MCP).
- 🤝 **Brands that want to offer fair deals** and close faster.

## Why use BVAL?

- **Priced from real views, the way each platform delivers them.** Instagram is priced on median Reel plays, TikTok on median plays (robust to viral outliers), YouTube on views of videos at a comparable age.
- **Each platform's value proposition is modelled.** Instagram: Reels plus Story link stickers and Partnership Ads. TikTok: cheaper reach, Spark Ads, a volatility check. YouTube: long-form integrations vs dedicated videos, description and pinned-comment links, Shorts.
- **Every right is a dated line item.** Usage, ads through the creator's handle and exclusivity are the terms brands slip in for free. BVAL prices each one separately.
- **Any country.** Brands pay by where the audience lives. BVAL applies a sourced market factor for 8 named markets (US, India, UK, Germany, Brazil, Indonesia, Mexico, Canada) and 13 regional groups covering every other country. Show prices in USD or local currency, with local tax and ad-disclosure notes.
- **Honest about uncertainty.** Industry sources disagree by 2–10x, so BVAL returns a range, a confidence level with reasons, and the sources behind every line.
- **Apify platform built in:** run it from the Console, the API, on a schedule, from Make / Zapier / n8n, or from any AI agent via the Apify MCP server.

## What data does BVAL return?

| Field | Example | Meaning |
|---|---|---|
| `verdict` | `COUNTER_TRADE_SCOPE` | ACCEPT_STRONG, ACCEPT, COUNTER_LIGHT, COUNTER_TRADE_SCOPE, DECLINE_OR_REDUCE_SCOPE, or NO_OFFER |
| `priceRange` | walk-away $910, floor $2,370, fair $2,790, ask $3,490 | Your negotiation range |
| `gapPct` | `71.4` | How far the offer is below fair value (%) |
| `lineItems` | Reel $990; Partnership Ads 30d $280; exclusivity 180d $1,360 | Every priced term, with sources and an assumption flag |
| `counterOptions` | full scope $3,490, or lighter $1,070 | The two-option close |
| `redFlags` | `LONG_EXCLUSIVITY`, `UNPRICED_WHITELISTING` | Lowball or risky terms detected |
| `counterEmail` | subject + body | Ready-to-send reply |
| `metrics` | 85,000 followers, median 42,000 plays, 3.5% ER | The data the price is based on |
| `confidence` | `medium` | With the reasons (sample size, clamping, fallbacks) |

A Markdown **quote report** (`QUOTE.md`) is also saved to the run's key-value store, ready to share.

## How to check a brand deal with BVAL

1. Open BVAL on Apify Store and click **Try for free**.
2. Choose the **platform** and paste the creator's **handle** or profile URL.
3. Pick the **niche** and the **deliverables** (for example 1 Instagram Reel, or 1 YouTube integration plus 1 Short).
4. Enter the **brand's offer** and the terms they asked for: usage days, ads through the handle, exclusivity days, rush, revisions and so on.
5. Set the **audience market** (ISO country code, or GLOBAL) and whether to show prices in USD or local currency.
6. Click **Start**. In about a minute you get the verdict, the range, the line items and the email.

Already know the creator's numbers? Fill **Manual metrics** to skip scraping and re-price new terms instantly.

## How much does BVAL cost?

BVAL uses **pay-per-event** pricing, so you pay only for results:

| Event | Price |
|---|---|
| Deal evaluated (scrape + full pricing + verdict) | **$0.79** |
| Counter-offer email drafted | **$0.20** |
| Deal re-priced with manual metrics (no scrape) | **$0.25** |

A full deal check with email costs **$0.99**. A manager checking 40 deals a month pays about $40. One better-negotiated deal usually covers a year of checks. You can cap spend per run with the maximum total charge setting.

## How the price is calculated

1. **Views basis:** median views of recent posts (Instagram Reels 3–120 days old, TikTok videos 3–120 days, YouTube long-form 30–365 days, Shorts 3–120 days). Missing play counts (0 or -1) are ignored, never treated as zero.
2. **Base:** `median views / 1000 × CPM × format ratio × niche multiplier`. CPMs per 1,000 views: Reels $20, TikTok $12, Shorts $8, YouTube integration $22 (dedicated video 2.5x).
3. **Engagement adjustment:** 0.80x–1.25x against tier benchmarks (HypeAuditor bands for Instagram).
4. **Tier band:** the price is kept inside published rate ranges for the creator's follower tier, so one viral post can't inflate it.
5. **Market:** multiplied by the audience country's factor (for example UK 0.85, Brazil 0.25, India 0.25 at micro tier).
6. **Add-ons** as % of the content base, by duration: organic usage (10–100%), paid usage (25–300%), Partnership/Spark Ads (35% for 30 days, 80% for 90 days), category exclusivity (30–150%, more in crowded niches, 2x if full exclusivity), rush (+35–50%), extra revisions, raw footage (+25%), cross-posting (+25%), link placements.
7. **Range:** fair = content + add-ons; ask = 1.25x fair; floor = 0.85x fair; walk-away = 0.85x the minimum scope (30-day usage, 7-day exclusivity, no ads).

Sources include LeadDyno/Aspire, Later, Influencer Marketing Hub, HypeAuditor, Modash, impact.com, Lumanu, Toptal, Net Influencer, upGrowth, Kolect and others. The full cited table ships with the Actor.

## Input example

```json
{
  "platform": "instagram",
  "handle": "examplecreator",
  "niche": "fitness",
  "deliverables": [{ "type": "instagram_reel", "qty": 1 }],
  "brandName": "Acme Protein",
  "offerAmount": 800,
  "offerCurrency": "USD",
  "organicUsageDays": 90,
  "whitelistingDays": 30,
  "exclusivityDays": 180,
  "market": "GLOBAL",
  "generateEmail": true
}
```

See the **Input** tab for every option. Deliverable types: `instagram_reel`, `instagram_story_frame`, `instagram_static_post`, `instagram_carousel`, `tiktok_video`, `youtube_integration`, `youtube_mention_15_30s`, `youtube_dedicated`, `youtube_short`.

## Output example

You can download the dataset as JSON, CSV, Excel or HTML, or read it through the API.

```json
{
  "handle": "examplecreator",
  "platform": "instagram",
  "verdict": "DECLINE_OR_REDUCE_SCOPE",
  "offerDisplay": "$800",
  "priceRange": { "walkAway": "$910", "floor": "$2,370", "fair": "$2,790", "ask": "$3,490" },
  "lineItems": [
    { "item": "1 x Instagram Reel", "amount": "$990" },
    { "item": "Organic usage rights, 90 days", "amount": "$160" },
    { "item": "Meta Partnership Ads (whitelisting), 30 days", "amount": "$280" },
    { "item": "Category exclusivity (fitness), 180 days", "amount": "$1,360" }
  ],
  "counterOptions": {
    "fullScope": { "price": "$3,490" },
    "reducedScope": { "price": "$1,070", "dropped": ["exclusivity", "whitelisting", "organic_usage"] }
  },
  "redFlags": [{ "code": "LONG_EXCLUSIVITY", "message": "Exclusivity beyond 7 days is worth +$1,364 on its own." }],
  "metrics": { "audience": 85000, "tier": "micro", "medianViews": 42000, "engagementRate": 0.035 },
  "confidence": "medium",
  "counterEmail": { "subject": "Re: Acme Protein partnership", "body": "Hi Acme Protein team, ..." }
}
```

## Use BVAL from an AI agent or the API

Every Apify Actor is available to AI agents through the [Apify MCP server](https://mcp.apify.com). Ask your agent *"Check this brand offer for @creator with BVAL"* and it can call BVAL directly. Agencies can also call it from the **API** tab, run it on a **schedule**, or connect it to **Make, Zapier or n8n** to check every inbound offer automatically.

## FAQ

### Is this financial or legal advice?
No. BVAL gives a benchmark-based estimate from public 2026 industry sources. Rates vary 2–10x across sources, so use the range as a negotiation anchor, not a guarantee.

### Why does the audience's country change the price?
Brands pay for the audience they reach. The same views are worth more to advertisers in the US than in Brazil or India. BVAL applies sourced market factors and covers every country through regional groups.

### Why is the price capped for very large creators?
Published rate tables top out below what the biggest celebrities charge. When the view-based price leaves the tier band, BVAL caps it and lowers the confidence level. It is built for creators from about 10K to 1M followers.

### TikTok in India?
TikTok has been blocked in India since 2020, so BVAL refuses that combination. China is not supported.

### Which data does BVAL scrape?
Only public profile and post metrics (followers, views, likes, comments) through Apify's official Store scrapers. Private accounts are not supported.

> Our Actors are ethical and do not extract any private user data, such as email addresses, gender, or location. They only extract what the user has chosen to share publicly. We therefore believe that our Actors, when used for ethical purposes by Apify users, are safe. However, you should be aware that your results could contain personal data. Personal data is protected by the GDPR in the European Union and by other regulations around the world. You should not scrape personal data unless you have a legitimate reason to do so. If you're unsure whether your reason is legitimate, consult your lawyers.

### Something looks wrong?
Open an issue in the **Issues** tab with the run link. Feedback on rates from your own deals is very welcome.

## Run locally

```bash
git clone https://github.com/arnavgupta28/BVAL.git && cd BVAL/bval
npm install -g apify-cli && apify login
python -m venv .venv && .venv/bin/pip install -r requirements.txt
apify run --input '{"platform":"instagram","handle":"examplecreator","offerAmount":800,"manualMetrics":{"followers":85000,"medianViews":42000,"engagementRate":0.035}}'
.venv/bin/python -m unittest discover -s tests   # 40 tests, including the research worked examples
```
