# Price creator deals from views, not followers

BVAL can be built today on defensible ground. Each deliverable is priced from **median recent views × a platform-and-format CPM**: $20 per 1K for Instagram Reels, $12 for TikTok videos, $8 for YouTube Shorts and $22 for a YouTube 60-90s integration, with a dedicated video at 2.5× an integration. That base is multiplied by a niche factor and clamped to a follower or subscriber tier band taken from published 2026 rate tables. Each deal term is then added as a percentage of base, using 2026 practitioner benchmarks.

The evidence for base rates and CPMs is moderate. Every source is a vendor or agency blog, and their ranges differ by 2-10×. The evidence for add-ons is thinner (expert roundups and search snippets). Several items have no published number at all, including link placement, cross-posting, full exclusivity, the floor multiplier, YouTube's comparable-age view anchor and TikTok/YouTube ER bands. They are marked `assumption` in the config.

The three platforms sell brands different things, and the engine models that. Instagram sells reach plus a conversion path through Stories and links, with Partnership Ads as the paid lever. TikTok sells cheap, high-variance reach with a short life, with Spark Ads as the paid lever. YouTube long-form sells durable, high-intent views, so it uses a different views anchor, a higher CPM, its own deliverable ladder and link-placement add-ons.

The market gap is not "another rate calculator": at least nine Apify pricing Actors and a dozen web calculators already exist. What nobody offers *as an API* is the full loop: the brand's offer goes in, and priced line items, a floor/ask/walk-away range, a verdict and a counter email come out. The three worked examples show the verdict range BVAL produces:

| Example | Fair value | Brand offer | Verdict |
|---|---|---|---|
| Instagram: 85k-follower fitness Reel creator | ~$2,793 | $800 | DECLINE OR REDUCE SCOPE |
| TikTok: 220k-follower beauty creator | ~$2,516 | $1,500 | COUNTER (trade scope) |
| YouTube: 180k-subscriber tech integration | ~$3,559 | $3,200 | COUNTER LIGHT |

---

## 1. Executive summary: a view-anchored, itemized model

**What the evidence supports.** Practitioners now anchor on views. TrySpansa's offer formula is niche CPM × (average views / 1,000) × format multiplier, and it calls subscriber count "the wrong one" to focus on ([TrySpansa](https://dev.to/tryspansa/influencer-rate-card-what-brands-should-pay-43oj)). Collabstr calls per-follower pricing weaker than fee ÷ expected views ([Collabstr](https://collabstr.com/blog/influencer-pay)). Sponsored CPMs on views run:

| Format | CPM range | Source |
|---|---|---|
| Instagram Reels | $15-45 | Modash |
| TikTok | $7-25 | Modash |
| YouTube integration | $15-35 | Modash |
| YouTube dedicated | $50-75+ | Modash |

The figures are from [Modash](https://www.modash.io/blog/influencer-marketing-cpm). LeadDyno's 2026 tables give tier bands: a micro Reel costs $500-2,500 and a mid Reel $2,500-6,000, with TikTok **40-50% below Reels** ([LeadDyno](https://www.leaddyno.com/blog/influencer-pricing)). Practitioners price add-ons as follows:

| Add-on | Typical price | Sources |
|---|---|---|
| Paid usage | 20-30% of base per 30 days | Net Influencer |
| Whitelisting | ~30% of base per 30 days | IMH |
| Category exclusivity | 30-50% for 30 days; 80-150% for 90 days | upGrowth |

Sources: [Net Influencer](https://www.netinfluencer.com/one-fee-no-expiration-33-creator-economy-professionals-on-whether-perpetual-usage-rights-are-ever-a-fair-deal/), [IMH](https://influencermarketinghub.com/organic-vs-paid-usage-rights/), [upGrowth](https://upgrowth.in/influencer-marketing-pricing-india-2026/).

**How strong it is.** Base rates and CPMs are moderate: several vendor sources converge. Usage, whitelisting and exclusivity are weak to moderate, because the expert roundups contradict each other. Some items have no source at all. No audited transaction dataset is public: Collabstr's report returned 403 during research, and FYPM and Fohr are paywalled.

**Key design decisions.**

| # | Decision | Why |
|---|---|---|
| D1 | Views are the anchor. Followers or subscribers only pick the tier and clamp the price | Supported by the sources above, and it separates BVAL from HypeAuditor, IMH, Collabstr and zaver |
| D2 | Each platform and format has its own views basis. IG Reels use `videoPlayCount → igPlayCount → videoViewCount`. TikTok uses `playCount`, excluding slideshows. YouTube long-form uses the median `viewCount` of videos **30-365 days old**. YouTube Shorts use the median Shorts `viewCount` | Each platform delivers value on a different timescale (section 2) |
| D3 | The engagement adjustment is capped at 0.80-1.25, has a per-platform formula and can be turned off | No source publishes an ER-to-price rule |
| D4 | Add-ons are a % of base. Usage-type add-ons are scaled by tier. Platform-specific add-ons are listed per platform, with an explicit `not_applicable` list | Mirrors how practitioners quote |
| D5 | **Ask** = 1.25 × fair. **Floor** = 0.85 × fair for the full scope. **Walk-away** = 0.85 × the price of a minimum scope | Encodes "trade scope, not price" |
| D6 | **Market** (global or India) is a separate input from **currency** (USD or INR) | A US rate converted to INR is not an Indian rate |
| D7 | The LLM email is generated from the computed line items only | No invented numbers |

---

## 2. Platform value propositions and how the engine prices each

The four formats sell brands different goods. BVAL captures this with five platform-specific settings: the **views basis** (which views, at what age), the **CPM**, the **deliverable ladder**, the **ER formula** and the **platform add-ons**. Swapping the CPM alone would not be enough.

| | Instagram (Reel; Stories, static and carousel as add-ons) | TikTok video | YouTube Shorts | YouTube long-form (integration or dedicated) |
|---|---|---|---|---|
| **What the brand buys** | Reach plus a conversion path (Story link stickers, link in bio). Bundles are the norm | Cheap, high-variance reach from trends and virality | Discovery reach at short-form prices | Durable, high-intent attention in a longer format |
| **Evidence** | IG is **40% of Collabstr campaigns**; Reels add **20-30%** over a feed post; Reel + Story + post = **1.6-2× a Reel**; Meta Partnership Ads gave **19% lower CPA, 13% higher CTR** | Rates are **40-50% below Reels**; TikTok-specific campaigns **fell 48%** in 2025 while UGC rose 133%; TikTok ER is higher than IG (Dash: 5.0% vs 3.6%) | Priced in the "lower range, similar to TikTok/Reels"; **0.4-0.6× an integration** | Integration CPM **$15-35**, niche spread **$6-55**; dedicated **$50-75+**; finance channels earn **3-5× gaming** |
| **Anchor metric** | Median Reel plays, posts 3-120 days old | Median plays, videos 3-120 days old, no slideshows. The median matters most because viral outliers skew the mean | Median Shorts views, Shorts 3-120 days old | Median long-form views of videos **30-365 days old**, so recent uploads are not undercounted. Not lifetime channel views (assumption) |
| **CPM (USD per 1K views)** | $20 | $12 | $8 | $22 for an integration; dedicated = 2.5× |
| **ER formula** | (likes + comments) / plays, using HypeAuditor tier bands | (diggCount + commentCount + shareCount) / playCount | Off (adjustment = 1.0) | (likes + commentsCount) / viewCount |
| **Main paid lever** | Partnership Ads (whitelisting factor 1.0) | Spark Ads (factor 0.85) | Paid usage of the asset | Paid usage of a cut-down; no handle whitelisting in v1 |
| **Platform add-ons** | Story frames (0.275× Reel), static (0.55×), carousel (0.75×), Story link sticker +10%, link in bio 7d +10% | Link in bio 7d +10%; volatility flag | Cross-post the Short to IG/TikTok +25% | Description link (included), pinned-comment link +5%, 15-30s mention (0.65×), dedicated (2.5×), Shorts cut-down cross-post +25% |
| **Not applicable** | Pinned comment, dedicated/mention ladder | Story stickers, static/carousel, pinned comment, dedicated ladder | Partnership/Spark factor, Story stickers, link in bio | Partnership/Spark factor, Story stickers, link in bio |

Sources for the evidence row: [Collabstr 2026](https://collabstr.com/2026-influencer-marketing-report), [Later](https://later.com/blog/influencer-pricing-benchmarks-the-complete-2026-guide/), [upGrowth](https://upgrowth.in/influencer-marketing-pricing-india-2026/), [Lumanu](https://www.lumanu.com/blog/how-influencers-charge-whitelisting-usage-rights), [LeadDyno](https://www.leaddyno.com/blog/influencer-pricing), [Dash Social](https://pages.dashsocial.com/hubfs/social-media-benchmark/2025/H2/all-industry.pdf), [TrySpansa](https://dev.to/tryspansa/influencer-rate-card-what-brands-should-pay-43oj), [Modash](https://www.modash.io/blog/influencer-marketing-cpm).

**Instagram.** The brand buys more than views. Reels compete for reach, while Stories and the bio link give a clickable path. Market practice reflects this: Later's micro bundle (feed post, Stories and basic usage) runs $1,000-3,000+, and Stories are priced about 50% below a feed post ([Later](https://later.com/blog/influencer-pricing-benchmarks-the-complete-2026-guide/)). Rate-card templates list link in bio as a separate add-on ([Selene the Lawyer](https://selenethelawyer.squarespace.com/blog/influencer-rate-card-template)), though no price is published, so +10% is an assumption. Partnership Ads are the dominant paid upsell. Snippet-level sources put them at **+50-100% versus +30-60% for Spark Ads** ([Sozee](https://sozee.ai/resources/influencer-whitelisting-rates-guide)), which is where the 1.0 versus 0.85 platform factor comes from. Story frames are priced from the Reel base because Stories are not scraped. That the brand buys conversion through stickers is an assumption: the notes contain no IG conversion-lift data beyond Lumanu's Partnership Ads figure.

**TikTok.** TikTok is the cheapest reach per view and the most volatile. The 40-50% discount to Reels is the best-supported platform gap in the data ([LeadDyno](https://www.leaddyno.com/blog/influencer-pricing)). The view-to-view variance and short shelf life (most plays in the first days) are **not documented in the notes**; they are working assumptions. They drive two design choices. First, use the median, never the mean. Second, report `volatility = p75/p25` of plays, and lower confidence when it exceeds 4 (assumption). HypeAuditor treats ~10% ER as "good" on TikTok, which is far above Instagram's view-based bands ([HypeAuditor](https://blog.hypeauditor.com/what-is-tiktok-engagement-rate-why-brands-should-take-note/)). BVAL therefore uses its own TikTok bands (low 3%, high 9%, an assumption) and includes shares in the formula. Demand is shifting: Collabstr saw TikTok-specific campaigns fall 48% in 2025 while UGC rose 133% ([Collabstr](https://collabstr.com/2026-influencer-marketing-report)). The README can position BVAL to price the UGC-style raw-footage and paid-usage add-ons that brands now buy.

**YouTube Shorts.** Shorts sit with TikTok and Reels on price. Later says they are priced in the lower range, and TrySpansa puts them at 0.4-0.6× an integration ([Later](https://later.com/blog/influencer-pricing-benchmarks-the-complete-2026-guide/), [TrySpansa](https://dev.to/tryspansa/influencer-rate-card-what-brands-should-pay-43oj)). Indian agencies price Shorts near Reels ([Grynow](https://www.grynow.in/blog/influencer-marketing-cost-in-india.html)). A Shorts CPM of $8 is about 0.36× the integration CPM, slightly below TrySpansa's ratio. It is labelled partly an assumption. ER is turned off for Shorts because no benchmark was found.

**YouTube long-form.** This format has the highest CPMs and the clearest niche spread: $6-15 for gaming up to $20-55 for finance ([TrySpansa](https://dev.to/tryspansa/influencer-rate-card-what-brands-should-pay-43oj)). Dedicated videos run $50-75+ CPM ([Modash](https://www.modash.io/blog/influencer-marketing-cpm)), or $0.05-0.10 per view ([Buffer citing Lumanu](https://buffer.com/resources/influencer-marketing-cost/)). Sources disagree on how much a dedicated video costs relative to an integration: 1.7-2× (LeadDyno) versus 3-5× (TrySpansa). BVAL uses **2.5×**. That long-form views keep accumulating for months, through search and suggested videos, is a widely held belief, but it is **not sourced in the notes**. BVAL hedges by anchoring on videos that are at least 30 days old, so a channel is not underpriced because of its fresh uploads. It does not credit lifetime totals. If fewer than 6 videos are that old, BVAL falls back to videos at least 7 days old and lowers confidence. The description link is treated as included in an integration and a pinned-comment link as +5% (both assumptions). Handle whitelisting is not modelled for YouTube in v1, so brand ad requests are priced as paid usage.

---

## 3. The pricing formula, step by step

**Step 0: Inputs.** Required: `platform` (`instagram`, `tiktok` or `youtube`), `handle`, `deliverables` (for example `[{"type":"instagram_reel","qty":1}]`), `niche`, and the brand's terms. The terms are:

- `organic_usage_days`, `paid_usage_days`
- `whitelisting_days`
- `exclusivity_days` and `exclusivity_scope`
- `rush_hours`, `revision_rounds`
- `raw_footage`
- `link_in_bio_days`, `story_link_stickers`, `pinned_comment_link`
- `cross_post_platforms`
- `payment_terms_days`, `deposit_pct`
- `perpetual`, `ai_training_clause`
- `offer_amount` and `offer_currency`

Optional: `market` (`global` or `india`), `output_currency`, `ad_spend_usd`, and `manual_metrics` to skip the scrape.

**Step 1: Views basis.** Scrape about 30 items per format and apply the platform rules from section 2. These are:

- the age window,
- dropping pinned posts, trial Reels and slideshows,
- the IG field fallback chain,
- treating `0`, `-1` and null as missing.

`median_views` needs at least 6 valid items. With fewer, use the feeder fallbacks in section 5 and lower the confidence.

**Step 2: Raw base.** `raw = median_views/1000 × cpm[format] × ratio[deliverable] × niche_mult`. Ratios cover formats priced off an anchor: IG Story 0.275, static 0.55 and carousel 0.75 off the Reel ([LeadDyno citing Aspire](https://www.leaddyno.com/blog/influencer-pricing)); YouTube mention 0.65 and dedicated 2.5 off the integration.

**Step 3: Engagement adjustment (design choice, flagged).** Compute ER with the platform formula and look up the `low`/`high` band for the creator's audience size. IG bands come from [HypeAuditor](https://hypeauditor.com/free-tools/instagram-engagement-calculator/). TikTok uses 3%/9% and YouTube long-form 2%/5%, both assumptions; the YouTube figures are anchored on Dash Social's ~3.4%. The adjustment `er_adj` is piecewise linear through four points (0 → 0.80, low → 1.00, high → 1.15, 2×high → 1.25), capped at 1.25. Use 1.0 if likes are hidden or ER is disabled. Sources only say ER places a creator high or low within a range ([Hootsuite](https://blog.hootsuite.com/influencer-pricing/)).

**Step 4: Tier clamp.** Tiers are nano 1K-10K, micro 10K-100K, mid 100K-500K, macro 500K-1M and mega 1M+, based on followers (IG, TikTok) or `numberOfSubscribers` (YouTube). Then `unit = clamp(raw × er_adj, min, max)`, where max is LeadDyno's top figure for that platform and tier, and min is 0.4 × LeadDyno's bottom figure (assumption). YouTube integration bands are LeadDyno's blended YouTube band × 0.55, since an integration is 50-60% of a dedicated video. Shorts bands are 0.5 × the Reel bands (assumption). Set `clamped:true` when the clamp fires. If no views are available, use $10 per 1K followers for IG ([Buffer](https://buffer.com/resources/influencer-marketing-cost/)) or $6 per 1K for TikTok (assumption). YouTube has no follower fallback; return an error asking for manual metrics.

**Step 5: Package.** `content_base = Σ unit × qty × (1 − discount)`. The discount is 10% for 2 deliverables, 15% for 3 or more, and capped at 25%. It applies to content only.

**Step 6: Add-ons, as % of `content_base`.**

- Organic usage, paid usage and whitelisting are multiplied by a tier factor: nano 0.6, micro 0.8, mid 1.0, macro 1.25, mega 1.5 ([impact.com](https://impact.com/influencer/how-much-to-charge-for-usage-rights-influencer/)).
- Durations round up to the next bucket.
- Paid usage is charged only beyond the whitelisting window: `paid(paid_days) − paid(whitelisting_days)`, with a minimum of 0.
- Whitelisting is multiplied by the platform factor (IG 1.0, TikTok 0.85; not offered on YouTube). If ad spend is given, use max(% fee, 3% of ad spend).
- Exclusivity = `category_pct × crowding × (2.0 if full scope)`, with a minimum of max($200, 15% of base).
- Rush, revisions, raw footage and cross-posting are flat percentages, as are the platform add-ons. Any add-on in a platform's `not_applicable` list is rejected with a warning.

**Step 7: Price points.**

- `fair` = content base + add-ons
- `ask` = 1.25 × fair ([Elev8or](https://www.elev8or.io/blog/how-to-negotiate-brand-deals), [Toptal](https://www.toptal.com/creator/post/usage-rights-for-creators))
- `floor` = 0.85 × fair (assumption)
- `walk_away` = 0.85 × the fair price of the **minimum scope**: same deliverables, 30-day organic usage, no paid usage or whitelisting, exclusivity of 7 days or less, standard turnaround

Display prices round to $10 or ₹500.

**Step 8: Verdict.**

| Offer | Verdict | Email strategy |
|---|---|---|
| ≥ ask | `ACCEPT_STRONG` | Confirm terms in writing |
| fair to ask | `ACCEPT` | Accept and restate scope |
| floor to fair | `COUNTER_LIGHT` | Counter at ask; settle at fair or above |
| walk-away to floor | `COUNTER_TRADE_SCOPE` | Full scope at ask, or reduced scope at their budget |
| < walk-away | `DECLINE_OR_REDUCE_SCOPE` | Warm decline, offering the minimum scope |

Also report `gap_pct = 1 − offer/fair`, the figure NegotiRate shows ([Product Hunt](https://www.producthunt.com/posts/1094453)).

**Step 9: INR and market.** INR output multiplies by `usd_inr` = 93.5. The rupee traded between 93.27 and 94.20 in mid-November 2026 ([HDFC Sky](https://hdfcsky.com/news/rupee-rises-24-paise-to-93-27-against-us-dollar-in-early-trade-november-18-2026), [HDFC Sky](https://hdfcsky.com/news/rupee-falls-8-paise-to-close-at-94-20-against-us-dollar)). Separately, `market=india` multiplies `unit` by an India tier factor **before** add-ons: nano 0.20, micro 0.25, mid 0.40, macro 0.55, mega 0.55. These factors are derived from Grynow and upGrowth INR ranges against LeadDyno's US bands, and agree with TrySpansa's 0.10-0.30 geo factor for lower tiers. GST at 18% can be shown as a separate line ([upGrowth](https://upgrowth.in/influencer-marketing-pricing-india-2026/)).

### Worked example A: Instagram Reel

The creator is @fitcreator, with 85,000 followers (micro tier), in fitness (multiplier 1.10). Median Reel plays are 42,000 across 24 valid Reels. View-based ER is 3.5%, against a HypeAuditor 50-100K band of 1.93% (low) to 5.12% (high). The brand asks for 1 Reel, 90 days of organic usage, 30 days of Partnership Ads and 180 days of category exclusivity (fitness is a crowded category). It offers **$800**.

| Step | Math | USD | INR (×93.5) |
|---|---|---|---|
| Raw | 42 × $20 × 1.0 × 1.10 | 924 | 86,394 |
| ER adjustment | 1 + 0.15 × (3.5−1.93)/(5.12−1.93) = **1.074** | | |
| Base | 924 × 1.074, within micro clamp [200, 2,500] | **992** | 92,772 |
| Organic usage, 90d | 20% × 0.8 tier = 16% | 159 | 14,844 |
| Partnership Ads, 30d | 35% × 0.8 × 1.0 = 28% | 278 | 25,976 |
| Category exclusivity, 180d | 110% × 1.25 crowded = 137.5% | 1,364 | 1,27,561 |
| **Fair value** | | **2,793** | **2,61,153** |
| **Ask / Floor** | ×1.25 / ×0.85 | **3,490 / 2,370** | **3,26,500 / 2,22,000** |
| **Walk-away** | (992 + 10%×0.8 organic 30d = 1,072) × 0.85 | **910** | **85,000** |
| Offer | $800 (₹74,800), 28.6% of fair | | |
| **Verdict** | Below walk-away → **DECLINE_OR_REDUCE_SCOPE** | | |

Two red flags fire: `LONG_EXCLUSIVITY` (the exclusivity alone is worth +$1,364) and `UNPRICED_WHITELISTING`. The counter offers full scope at $3,490, or a Reel with 30-day organic usage and 7-day exclusivity at about $1,070. Adding 3 Story frames with link stickers to that offer would add 3 × (0.275 × 992 × 1.10) ≈ $900 before the package discount. With `market=india`, fair value drops to $698 (₹65,300) and the $800 offer becomes **ACCEPT**. Market therefore has to be an explicit input.

### Worked example B: TikTok video

The creator is @glowtok, with 220,000 followers (mid tier), in beauty (multiplier 1.0). Median `playCount` is 95,000 across 28 non-slideshow videos, and p75/p25 is 2.6, so no volatility flag. ER, computed as (digg + comment + share)/play, is 7.2% against bands of 3% (low) and 9% (high). The brand asks for 1 video, 30 days of Spark Ads, 60 days of paid usage, delivery within 48 hours, 2 revision rounds and 7 days of exclusivity. It offers **$1,500**.

| Step | Math | USD | INR (×93.5) |
|---|---|---|---|
| Raw | 95 × $12 × 1.0 × 1.0 | 1,140 | 1,06,590 |
| ER adjustment | 1 + 0.15 × (7.2−3)/(9−3) = **1.105** | | |
| Base | within TikTok mid clamp [600, 3,500] | **1,260** | 1,17,782 |
| Spark Ads, 30d | 35% × 1.0 × 0.85 = 29.75% | 375 | 35,040 |
| Paid usage, 60d | paid(60) − paid(30) = 20% | 252 | 23,556 |
| Rush, under 72h | 35% | 441 | 41,224 |
| Extra revision round | max(15%, $150) | 189 | 17,667 |
| Exclusivity, 7d | free window | 0 | 0 |
| **Fair value** | | **2,516** | **2,35,269** |
| **Ask / Floor** | ×1.25 / ×0.85 | **3,150 / 2,140** | **2,94,000 / 2,00,000** |
| **Walk-away** | (1,260 × 1.10) × 0.85 | **1,180** | **1,10,000** |
| Offer | $1,500, 59.6% of fair | | |
| **Verdict** | Between walk-away and floor → **COUNTER_TRADE_SCOPE** | | |

The counter offers full scope at $3,150, or 30 days of Spark Ads only, standard turnaround and 1 revision round at **$1,635**.

### Worked example C: YouTube integration

The channel is @techreviews, with 180,000 subscribers (mid tier), in tech (multiplier 1.45). Of the 30 latest long-form videos, 22 are 30-365 days old, with a median `viewCount` of 60,000. ER, computed as (likes + comments)/views, is 4.2% against bands of 2% (low) and 5% (high). The brand asks for 1 integration of 60-90 seconds, a description link plus a pinned-comment link, 30 days of paid usage of a cut-down, and 30 days of category exclusivity (tech is a crowded category). It offers **$3,200**.

| Step | Math | USD | INR (×93.5) |
|---|---|---|---|
| Raw | 60 × $22 × 1.0 × 1.45 | 1,914 | 1,78,959 |
| ER adjustment | 1 + 0.15 × (4.2−2)/(5−2) = **1.11** | | |
| Base | within YouTube integration mid clamp [1,980, 13,750] | **2,125** | 1,98,644 |
| Description link | included | 0 | 0 |
| Pinned-comment link | 5% | 106 | 9,932 |
| Paid usage, 30d | 25% × 1.0 | 531 | 49,661 |
| Category exclusivity, 30d | 30% × 1.25 = 37.5% | 797 | 74,492 |
| **Fair value** | | **3,559** | **3,32,730** |
| **Ask / Floor** | ×1.25 / ×0.85 | **4,450 / 3,020** | **4,16,000 / 2,83,000** |
| **Walk-away** | (2,125 × 1.10) × 0.85 | **1,990** | **1,85,500** |
| Offer | $3,200 (₹2,99,200), 89.9% of fair | | |
| **Verdict** | Between floor and fair → **COUNTER_LIGHT** | | |

The counter is $4,450, settling at $3,560 or more. Dropping the paid usage instead brings fair value to about $3,030, which the brand's $3,200 already covers.

---

## 4. Proposed `rates.json`

A path in `sources` covers every numeric field beneath it unless a more specific path exists. Source IDs resolve to section 11. `assumption` marks BVAL's own design choice or interpolation.

```json
{
  "version": "2026-11-22.2",
  "currency": {
    "base": "USD",
    "usd_inr": 93.5,
    "rounding": { "usd": 10, "inr": 500 },
    "india_market_factor_by_tier": { "nano": 0.20, "micro": 0.25, "mid": 0.40, "macro": 0.55, "mega": 0.55 },
    "india_gst_pct": 18
  },
  "tier_bounds": {
    "nano": [1000, 10000], "micro": [10000, 100000], "mid": [100000, 500000],
    "macro": [500000, 1000000], "mega": [1000000, null]
  },
  "engagement_curve": { "at_zero": 0.80, "at_low": 1.00, "at_high": 1.15, "at_2x_high": 1.25, "cap": 1.25, "hidden_likes_adj": 1.0 },
  "platforms": {
    "instagram": {
      "audience_metric": "followersCount",
      "sampling": { "items": 30, "min_valid": 6, "min_age_days": 3, "max_age_days": 120 },
      "deliverables": {
        "instagram_reel": {
          "cpm_usd": 20, "ratio": 1.0,
          "views_basis": "median(videoPlayCount>igPlayCount>videoViewCount), productType=clips",
          "clamp_usd": { "nano": [100, 500], "micro": [200, 2500], "mid": [1000, 6000], "macro": [2400, 10000], "mega": [4000, 50000] }
        },
        "instagram_story_frame": { "priced_from": "instagram_reel", "ratio": 0.275, "optional": true },
        "instagram_static_post": { "priced_from": "instagram_reel", "ratio": 0.55, "optional": true },
        "instagram_carousel": { "priced_from": "instagram_reel", "ratio": 0.75, "optional": true }
      },
      "engagement": {
        "enabled": true,
        "formula": "(likesCount + commentsCount) / views",
        "bands": [
          { "audience": [0, 10000],        "low": 0.0228, "high": 0.0607 },
          { "audience": [10000, 50000],    "low": 0.0202, "high": 0.0537 },
          { "audience": [50000, 100000],   "low": 0.0193, "high": 0.0512 },
          { "audience": [100000, 500000],  "low": 0.0190, "high": 0.0506 },
          { "audience": [500000, 1000000], "low": 0.0200, "high": 0.0532 },
          { "audience": [1000000, null],   "low": 0.0170, "high": 0.0452 }
        ]
      },
      "follower_fallback_usd_per_1k": 10,
      "platform_addons": {
        "whitelisting_name": "meta_partnership_ads",
        "whitelisting_factor": 1.0,
        "link_in_bio_7d_pct": 10,
        "story_link_sticker_pct": 10
      },
      "not_applicable": ["pinned_comment_link", "youtube_dedicated", "youtube_mention"]
    },
    "tiktok": {
      "audience_metric": "authorMeta.fans",
      "sampling": { "items": 30, "min_valid": 6, "min_age_days": 3, "max_age_days": 120, "volatility_flag_p75_p25": 4.0 },
      "deliverables": {
        "tiktok_video": {
          "cpm_usd": 12, "ratio": 1.0,
          "views_basis": "median(playCount), isSlideshow=false",
          "clamp_usd": { "nano": [50, 250], "micro": [100, 1500], "mid": [600, 3500], "macro": [1400, 6000], "mega": [2800, 20000] }
        }
      },
      "engagement": {
        "enabled": true,
        "formula": "(diggCount + commentCount + shareCount) / playCount",
        "bands": [ { "audience": [0, null], "low": 0.03, "high": 0.09 } ]
      },
      "follower_fallback_usd_per_1k": 6,
      "platform_addons": {
        "whitelisting_name": "tiktok_spark_ads",
        "whitelisting_factor": 0.85,
        "link_in_bio_7d_pct": 10
      },
      "not_applicable": ["story_link_sticker", "pinned_comment_link", "instagram_static_post", "instagram_carousel", "youtube_dedicated"]
    },
    "youtube": {
      "audience_metric": "numberOfSubscribers",
      "sampling": {
        "long_form": { "items": 30, "min_valid": 6, "min_age_days": 30, "max_age_days": 365, "fallback_min_age_days": 7 },
        "shorts": { "items": 30, "min_valid": 6, "min_age_days": 3, "max_age_days": 120 }
      },
      "deliverables": {
        "youtube_integration": {
          "cpm_usd": 22, "ratio": 1.0,
          "views_basis": "median(viewCount), type=video, age 30-365d",
          "clamp_usd": { "nano": [45, 550], "micro": [220, 5500], "mid": [1980, 13750], "macro": [2200, 27500], "mega": [4400, 55000] }
        },
        "youtube_mention_15_30s": { "priced_from": "youtube_integration", "ratio": 0.65 },
        "youtube_dedicated": { "priced_from": "youtube_integration", "ratio": 2.5, "clamp_rule": "integration_clamp_x_ratio" },
        "youtube_short": {
          "cpm_usd": 8, "ratio": 1.0,
          "views_basis": "median(viewCount), type=shorts, age 3-120d",
          "clamp_usd": { "nano": [50, 250], "micro": [100, 1250], "mid": [500, 3000], "macro": [1200, 5000], "mega": [2000, 25000] }
        }
      },
      "engagement": {
        "long_form": { "enabled": true, "formula": "(likes + commentsCount) / viewCount", "bands": [ { "audience": [0, null], "low": 0.02, "high": 0.05 } ] },
        "shorts": { "enabled": false }
      },
      "follower_fallback_usd_per_1k": null,
      "platform_addons": {
        "whitelisting_name": null,
        "description_link_pct": 0,
        "pinned_comment_link_pct": 5
      },
      "not_applicable": ["whitelisting", "story_link_sticker", "link_in_bio", "instagram_static_post", "instagram_carousel"]
    }
  },
  "niche_multipliers": {
    "finance": 1.9, "business_saas": 1.6, "tech": 1.45, "education": 1.25,
    "health": 1.15, "health_credentialed": 1.5, "fitness": 1.1, "beauty": 1.0,
    "fashion": 1.0, "travel": 1.1, "lifestyle": 1.0, "food": 0.9, "parenting": 0.95,
    "entertainment": 0.7, "gaming": 0.55, "other": 1.0,
    "india_overrides": { "beauty": 1.2 }
  },
  "addons": {
    "usage_tier_multiplier": { "nano": 0.6, "micro": 0.8, "mid": 1.0, "macro": 1.25, "mega": 1.5 },
    "organic_usage_pct": { "30": 10, "60": 15, "90": 20, "180": 30, "365": 50, "perpetual": 100 },
    "organic_extra_owned_channel_pct": 10,
    "paid_usage_pct": { "30": 25, "60": 45, "90": 60, "180": 90, "365": 125, "perpetual": 300 },
    "whitelisting_pct": { "30": 35, "60": 60, "90": 80, "each_extra_30": 25 },
    "whitelisting_ad_spend_pct": 3,
    "whitelisting_min_usd_per_30d": 100,
    "exclusivity_category_pct": { "7": 0, "30": 30, "90": 75, "180": 110, "365": 150 },
    "exclusivity_full_factor": 2.0,
    "exclusivity_crowding_factor": { "crowded": 1.25, "standard": 1.0, "niche": 0.75 },
    "crowded_categories": ["beauty", "fashion", "fitness", "tech", "food"],
    "exclusivity_min_usd": 200,
    "exclusivity_min_pct_of_base": 15,
    "rush_pct": { "under_72h": 35, "under_24h": 50 },
    "revisions": { "included_rounds": 1, "extra_round_pct": 15, "extra_round_min_usd": 150 },
    "raw_footage_pct": 25,
    "cross_post_pct_per_platform": 25,
    "buyout_rule": "paid_usage_pct.perpetual + raw_footage_pct"
  },
  "package_discounts_pct": { "2": 10, "3_plus": 15, "max": 25 },
  "negotiation": {
    "ask_mult": 1.25,
    "floor_mult": 0.85,
    "walk_away_mult_of_min_scope": 0.85,
    "min_scope": { "organic_usage_days": 30, "paid_usage_days": 0, "whitelisting_days": 0, "exclusivity_days": 7, "rush": false },
    "verdict_thresholds": {
      "ACCEPT_STRONG": "offer >= ask",
      "ACCEPT": "offer >= fair",
      "COUNTER_LIGHT": "offer >= floor",
      "COUNTER_TRADE_SCOPE": "offer >= walk_away",
      "DECLINE_OR_REDUCE_SCOPE": "offer < walk_away"
    },
    "red_flag_limits": {
      "paid_usage_days_overbuy": 180,
      "exclusivity_days_unpaid_max": 7,
      "payment_terms_days_max": 60,
      "deposit_pct_min": 50,
      "included_revisions_max": 2
    }
  },
  "sources": {
    "currency.usd_inr": ["hdfc_fx_1", "hdfc_fx_2"],
    "currency.india_market_factor_by_tier": ["grynow", "upgrowth", "leaddyno", "tryspansa", "assumption"],
    "currency.india_gst_pct": ["upgrowth"],
    "tier_bounds": ["leaddyno", "grynow"],
    "engagement_curve": ["hootsuite", "later2026", "assumption"],
    "platforms.instagram.sampling": ["assumption"],
    "platforms.instagram.deliverables.instagram_reel.cpm_usd": ["modash_cpm", "imh_ig", "iqfluence"],
    "platforms.instagram.deliverables.instagram_reel.ratio": ["assumption"],
    "platforms.instagram.deliverables.instagram_reel.clamp_usd": ["leaddyno", "later2026", "assumption"],
    "platforms.instagram.deliverables.instagram_story_frame": ["leaddyno", "later2026"],
    "platforms.instagram.deliverables.instagram_static_post": ["leaddyno"],
    "platforms.instagram.deliverables.instagram_carousel": ["leaddyno", "assumption"],
    "platforms.instagram.engagement.bands": ["hypeauditor_er"],
    "platforms.instagram.follower_fallback_usd_per_1k": ["buffer_cost", "collabstr_pay"],
    "platforms.instagram.platform_addons.whitelisting_factor": ["sozee_wl", "lumanu", "assumption"],
    "platforms.instagram.platform_addons.link_in_bio_7d_pct": ["selene", "assumption"],
    "platforms.instagram.platform_addons.story_link_sticker_pct": ["assumption"],
    "platforms.tiktok.sampling": ["assumption"],
    "platforms.tiktok.deliverables.tiktok_video.cpm_usd": ["modash_cpm", "leaddyno"],
    "platforms.tiktok.deliverables.tiktok_video.ratio": ["assumption"],
    "platforms.tiktok.deliverables.tiktok_video.clamp_usd": ["leaddyno", "assumption"],
    "platforms.tiktok.engagement.bands": ["hypeauditor_tt", "dash_social", "assumption"],
    "platforms.tiktok.follower_fallback_usd_per_1k": ["leaddyno", "assumption"],
    "platforms.tiktok.platform_addons.whitelisting_factor": ["sozee_wl", "assumption"],
    "platforms.tiktok.platform_addons.link_in_bio_7d_pct": ["assumption"],
    "platforms.youtube.sampling": ["assumption"],
    "platforms.youtube.deliverables.youtube_integration.cpm_usd": ["tryspansa", "creatordb_aol", "modash_cpm"],
    "platforms.youtube.deliverables.youtube_integration.ratio": ["assumption"],
    "platforms.youtube.deliverables.youtube_integration.clamp_usd": ["leaddyno", "impact_yt", "assumption"],
    "platforms.youtube.deliverables.youtube_mention_15_30s": ["tryspansa"],
    "platforms.youtube.deliverables.youtube_dedicated": ["leaddyno", "tryspansa", "modash_cpm"],
    "platforms.youtube.deliverables.youtube_short.cpm_usd": ["tryspansa", "later2026", "assumption"],
    "platforms.youtube.deliverables.youtube_short.ratio": ["assumption"],
    "platforms.youtube.deliverables.youtube_short.clamp_usd": ["later2026", "assumption"],
    "platforms.youtube.engagement.long_form.bands": ["dash_social", "assumption"],
    "platforms.youtube.platform_addons": ["assumption"],
    "niche_multipliers": ["tryspansa", "leaddyno"],
    "niche_multipliers.travel": ["tryspansa", "leaddyno", "assumption"],
    "niche_multipliers.parenting": ["tryspansa", "leaddyno", "assumption"],
    "niche_multipliers.other": ["assumption"],
    "niche_multipliers.india_overrides.beauty": ["upgrowth"],
    "addons.usage_tier_multiplier": ["impact_usage"],
    "addons.organic_usage_pct": ["toptal_usage", "imh_usage", "upgrowth", "assumption"],
    "addons.organic_extra_owned_channel_pct": ["imh_usage", "toptal_usage"],
    "addons.paid_usage_pct": ["netinf_33", "netinf_23", "stack", "assumption"],
    "addons.whitelisting_pct": ["imh_usage", "netinf_23", "upgrowth", "assumption"],
    "addons.whitelisting_ad_spend_pct": ["lumanu", "toptal_usage"],
    "addons.whitelisting_min_usd_per_30d": ["socialync", "assumption"],
    "addons.exclusivity_category_pct": ["upgrowth", "toptal_usage", "impact_usage", "creatorsjet", "modash_excl"],
    "addons.exclusivity_full_factor": ["netinf_23", "assumption"],
    "addons.exclusivity_crowding_factor": ["modash_excl", "assumption"],
    "addons.exclusivity_min_usd": ["modash_excl"],
    "addons.exclusivity_min_pct_of_base": ["assumption"],
    "addons.rush_pct": ["influenceflow", "assumption"],
    "addons.revisions": ["upgrowth", "backstage", "stack"],
    "addons.raw_footage_pct": ["imh_usage"],
    "addons.cross_post_pct_per_platform": ["modash_bundling", "assumption"],
    "package_discounts_pct": ["templatenet", "upgrowth", "modash_bundling", "assumption"],
    "negotiation.ask_mult": ["elev8or", "toptal_usage"],
    "negotiation.floor_mult": ["assumption"],
    "negotiation.walk_away_mult_of_min_scope": ["assumption"],
    "negotiation.min_scope": ["beacons", "modash_excl", "assumption"],
    "negotiation.red_flag_limits.paid_usage_days_overbuy": ["netinf_23", "assumption"],
    "negotiation.red_flag_limits.exclusivity_days_unpaid_max": ["modash_excl"],
    "negotiation.red_flag_limits.payment_terms_days_max": ["elev8or", "assumption"],
    "negotiation.red_flag_limits.deposit_pct_min": ["elev8or"],
    "negotiation.red_flag_limits.included_revisions_max": ["assumption"]
  }
}
```

**Implementation notes:**

- **Duration buckets.** Use the smallest bucket that is at least the requested duration. More than 365 days, or `perpetual`, maps to the `perpetual` value and raises the `PERPETUAL` flag.
- **Whitelisting past 90 days.** Add `each_extra_30` for each started 30 days.
- **Dedicated YouTube videos.** These inherit the integration's views basis, CPM and clamp, multiplied by 2.5.
- **Mixed deals** (for example an IG Reel plus a TikTok cross-post). Price the primary platform's deliverable, then add `cross_post_pct_per_platform` instead of re-scraping the second platform.

---

## 5. Feeder actors per platform

### Instagram: profile scraper plus Reel scraper

| Purpose | Actor ID | Input | Fields |
|---|---|---|---|
| Followers | `apify/instagram-profile-scraper` | `{"usernames": ["<h>"]}` | `followersCount`, `private`, `verified`, `error` |
| Reel plays and engagement | `apify/instagram-reel-scraper` | `{"username": ["<h>"], "resultsLimit": 30, "skipPinnedPosts": true, "skipTrialReels": true}` | `videoPlayCount` → `igPlayCount` → `videoViewCount`; `likesCount` (-1 means hidden), `commentsCount`, `timestamp`, `productType`, `paidPartnership` |

**Why the Reel scraper and not the post scraper.**

- **Every item is usable.** All 30 items are Reels, while the post scraper's mixed feed can leave few `clips` once images and carousels are filtered out.
- **Play counts are documented.** Its README samples show `videoPlayCount` populated (`"videoViewCount": 45600, "videoPlayCount": 809683`).
- **Trial Reels can be excluded.** It has `skipTrialReels`, and trial Reels are not flagged in the output ([README](https://apify.com/apify/instagram-reel-scraper.md)).
- **The post scraper's cheap mode is unverified.** Its `basicData` mode does not say whether it includes `videoPlayCount`, and its schema defaults to the pricier `detailedData` ([README](https://apify.com/apify/instagram-post-scraper.md)).
- **The profile scraper is not a views source.** Its `latestPosts` is capped at 12 items and shows only `videoViewCount` ([README](https://apify.com/apify/instagram-profile-scraper.md)), which the schemas mark "Deprecated by Instagram; may be null or stale" ([schema](https://api.apify.com/v2/acts/apify~instagram-reel-scraper/builds/default)).

**Fallbacks:**

1. Use the Reel scraper. Treat `0`, `-1` and null as missing, and record which field was used.
2. If fewer than 6 Reels are valid, run the post scraper with `{"username":[h],"resultsLimit":30,"skipPinnedPosts":true,"dataDetailLevel":"detailedData"}` and filter to `productType=="clips"`.
3. If that also fails, use the profile scraper's `latestPosts[].videoViewCount` and set confidence to low.
4. As a last resort, use the follower rate of $10 per 1K and set confidence to very low.

The fallbacks exist because public issues report `videoPlayCount` returning 0 or going missing ([issue](https://apify.com/apify/instagram-reel-scraper/issues/videoplaycount--0-li-JW5XPst0hWkYESA70), [issue](https://apify.com/apify/instagram-post-scraper/issues/video-play-counts-mi-Z9MLa1rezMru0ltev)).

**Cost per creator.** On the FREE tier, $0.0026 + 30 × $0.0026 + $0.001 ≈ **$0.082**. On SILVER, about $0.045 ([pricing](https://api.apify.com/v2/acts/apify~instagram-reel-scraper), [pricing](https://api.apify.com/v2/acts/apify~instagram-profile-scraper)).

### TikTok: clockworks/tiktok-profile-scraper

**Input:** `{"profiles": ["<h>"], "resultsPerPage": 30, "profileSorting": "latest", "excludePinnedPosts": true}`. The default `resultsPerPage` is 100. Avoid date filters, which are charged per item.

**Fields used:**

- Views and engagement: `playCount`, `diggCount`, `commentCount`, `shareCount`, `collectCount`
- Filtering: `createTimeISO`, `isSlideshow` (exclude these), `isPinned`, `isSponsored`
- Account: `authorMeta.fans` (followers, from the first item), `authorMeta.privateAccount`
- Errors: `error` / `errorCode`

**Cost per creator:** about **$0.09** on FREE (30 × $0.003) and $0.045 on SILVER. There is no minimum charge, whereas `clockworks/tiktok-scraper` has a $0.50 minimum and a default `resultsPerPage` of 1 ([API](https://api.apify.com/v2/acts/clockworks~tiktok-profile-scraper), [API](https://api.apify.com/v2/acts/clockworks~tiktok-scraper)).

**Fallbacks:** `clockworks/tiktok-scraper` with `profiles` and `resultsPerPage: 30`, then the follower rate.

### YouTube: streamers/youtube-scraper

**Input:** `{"startUrls":[{"url":"https://www.youtube.com/@<h>"}],"maxResults":30,"maxResultsShorts":30,"maxResultStreams":0,"sortVideosBy":"NEWEST"}`. Set `maxResultsShorts: 0` unless a Short is among the deliverables.

**Processing:** Split results by `type` (`video` / `shorts`). Read `viewCount`, `likes`, `commentsCount`, `date` (handle both ISO and date-only formats), `numberOfSubscribers` and `error` codes such as `CHANNEL_DOES_NOT_EXIST`. Compute each video's age from `date` to apply the 30-365 day long-form window.

**Coverage caveat:** For channels that upload daily, 30 NEWEST videos may contain fewer than 6 that are 30 or more days old. Use the 7-day fallback, or raise `maxResults` to 60.

**Cost per creator:** $0.12 (long-form only) to $0.24 on FREE, at $0.004 per video. `streamers/youtube-channel-scraper` costs $0.0013 per video but lacks likes and comments and returns relative dates ("23 hours ago"), so use it only as a views-only fallback ([README](https://apify.com/streamers/youtube-scraper.md), [README](https://apify.com/streamers/youtube-channel-scraper.md)).

### Python SDK call pattern

```python
import asyncio, statistics
from datetime import datetime, timezone, timedelta
from apify import Actor

async def run_feeder(actor_id: str, run_input: dict) -> list[dict]:
    # Documented: Actor.call waits for the run to finish.
    # TODO verify kwarg names before adding: timeout=timedelta(seconds=90), memory_mbytes=1024, max_total_charge_usd=0.30
    run = await Actor.call(actor_id=actor_id, run_input=run_input)
    if run is None:
        return []
    page = await Actor.apify_client.run(run.id).dataset().list_items()
    return [i for i in page.items if not i.get("error")]

def age_days(ts: str) -> float:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None:                     # YouTube may return date-only strings
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).total_seconds() / 86400

def ig_views(item):
    for key in ("videoPlayCount", "igPlayCount", "videoViewCount"):
        v = item.get(key)
        if isinstance(v, (int, float)) and v > 0:
            return v, key
    return None, None

async def scrape_instagram(h):
    profile, reels = await asyncio.gather(   # parallel: latency = slower run, not the sum
        run_feeder("apify/instagram-profile-scraper", {"usernames": [h]}),
        run_feeder("apify/instagram-reel-scraper", {"username": [h], "resultsLimit": 30,
                                                   "skipPinnedPosts": True, "skipTrialReels": True}))
    followers = profile[0]["followersCount"] if profile else None
    rows = []
    for r in reels:
        v, field = ig_views(r)
        if v and 3 <= age_days(r["timestamp"]) <= 120:
            likes = r.get("likesCount", -1)
            rows.append({"views": v, "field": field,
                         "er": (likes + r.get("commentsCount", 0)) / v if likes >= 0 else None})
    return followers, rows

async def scrape_tiktok(h):
    items = await run_feeder("clockworks/tiktok-profile-scraper",
        {"profiles": [h], "resultsPerPage": 30, "profileSorting": "latest", "excludePinnedPosts": True})
    followers = items[0]["authorMeta"]["fans"] if items else None
    rows = [{"views": i["playCount"],
             "er": (i.get("diggCount", 0) + i.get("commentCount", 0) + i.get("shareCount", 0)) / i["playCount"]}
            for i in items
            if not i.get("isSlideshow") and (i.get("playCount") or 0) > 0 and 3 <= age_days(i["createTimeISO"]) <= 120]
    return followers, rows

async def scrape_youtube(h, want_shorts: bool):
    items = await run_feeder("streamers/youtube-scraper", {
        "startUrls": [{"url": f"https://www.youtube.com/@{h}"}], "maxResults": 30,
        "maxResultsShorts": 30 if want_shorts else 0, "maxResultStreams": 0, "sortVideosBy": "NEWEST"})
    subs = next((i.get("numberOfSubscribers") for i in items if i.get("numberOfSubscribers")), None)
    def rows(kind, lo, hi):
        out = []
        for i in items:
            if i.get("type") == kind and (i.get("viewCount") or 0) > 0 and i.get("date") and lo <= age_days(i["date"]) <= hi:
                er = (i.get("likes", 0) + i.get("commentsCount", 0)) / i["viewCount"]
                out.append({"views": i["viewCount"], "er": er})
        return out
    long_rows = rows("video", 30, 365)
    if len(long_rows) < 6:
        long_rows = rows("video", 7, 365)    # fallback, lower confidence
    return subs, long_rows, rows("shorts", 3, 120)
```

The `Actor.call` and `list_items().items` pattern is from the [Apify Python SDK docs](https://docs.apify.com/sdk/python/docs/concepts/interacting-with-other-actors.md). Charge PPE events with `await Actor.charge(event_name="deal-evaluated")`, after verifying the signature.

---

## 6. Competitive landscape: the pieces exist, the combination doesn't

| Tool | Type / price | Priced from | Itemized usage / whitelist / exclusivity | Offer → verdict | Counter email | Floor/ask/walk | API | Platforms | INR |
|---|---|---|---|---|---|---|---|---|---|
| **BVAL** | Apify Actor, ~$0.99 per deal | Scraped median views, platform-specific | Yes, any duration; Partnership/Spark factors; YouTube link placement | 5 levels | Yes | Yes | Actor + MCP | IG, TikTok, YouTube (Shorts and long-form) | Yes, plus India mode |
| [hypebridge/hypebridge-pricing](https://apify.com/hypebridge/hypebridge-pricing) | Actor, ~$0.25 + $1.70 ≈ **$1.95 per handle**; 1 monthly user | Handle via AI evaluation | Fixed 30/90/365-day usage; 30-day whitelisting and exclusivity | No | No | No | Yes | IG, TikTok | No |
| [kayhermes/creator-sponsorship-rate-estimator](https://apify.com/kayhermes/creator-sponsorship-rate-estimator) | Actor, $5 per 1K | User-supplied metrics | Yes | No | No | Low/mid/high | Yes | Multi | No |
| [apricot_blackberry/rate-card-generator](https://apify.com/apricot_blackberry/rate-card-generator) | Actor, $15 per 1K | CPM | Usage and exclusivity only | No ("not a fair price") | No | No | Yes | YT, IG, TikTok | No |
| [zaver.api/instagram-influencer-price-calculator](https://apify.com/zaver.api/instagram-influencer-price-calculator) | Actor, $79.90 per 1K | IG metrics | Excluded | No | No | Range | Yes | IG | No |
| [trovevault/influencer-pricing-calculator](https://apify.com/trovevault/influencer-pricing-calculator) | Actor, PPE | Followers / ER | Excluded | No | No | ±20% | Yes | 8 platforms | No |
| [HypeAuditor calculator](https://hypeauditor.com/free-tools/instagram-pricing-calculator/) | Free web | Followers + ER | Usage duration, whitelisting yes/no, exclusivity | No | No | Range | Separate paid API | IG | No |
| [NegotiRate](https://www.producthunt.com/posts/1094453) | Web; £25 report | Views, engagement, niche | Usage as input, not lines | Underpay % | Paid | No | No | TikTok, IG, YT, UGC | No |
| [CreatorFlowX](https://www.producthunt.com/products/creatorflowx/makers) | Web | Views, engagement | Exclusivity input | Weak/fair/strong | Yes | No | No | Multi | No |
| [Sovaio](https://www.producthunt.com/products/sovaio/reviews) | Web, free | YouTube Studio upload | Not mentioned | Yes | Drafts | No | No | YouTube only | No |
| [Collabstr calculator](https://collabstr.com/influencer-price-calculator) | Free web | Marketplace asking prices | No | No | No | Average | No | Multi | No |
| [IMH calculator](https://nealschaffer.com/instagram-influencer-calculators/) | Free web | Followers, ER | No | No | No | Range | No | IG | No |
| [Qoruz cost checker](https://qoruz.com/tools/influencer-cost-checker) | Free web (India) | IG handle | No | No | No | Single figure | No | IG | Likely |

**The gap.** The Apify pricing Actors return rate cards but take no offer. In the top 50 results for 13 Store queries, the phrases "counter offer" and "walk away" appear nowhere. The consumer apps that do give a verdict and a counter (NegotiRate, CreatorFlowX, Sovaio) have no API and don't itemize terms. No tool names Spark Ads or Partnership Ads as priced lines, and none prices YouTube link placement or applies a comparable-age view anchor. Indian platforms sell managed campaigns with pricing on request ([Elev8or India](https://www.elev8or.io/blog/best-influencer-marketing-platforms-in-india)). Demand sits with the scrapers, not with pricing Actors, which have 0-2 monthly users each. Position BVAL as a **deal-decision tool**, and don't claim it is the first counter-offer generator.

**README lines:**

- "Paste the brand's offer. Get the verdict, your floor/ask/walk-away, and a counter email that itemizes every right."
- "Priced from real views, measured the way each platform delivers them: Reel plays, TikTok plays, and YouTube views at comparable age, not follower counts."
- "Partnership Ads, Spark Ads, usage, exclusivity, rush and link placement: each a dated line item with a cited benchmark."
- "Agent-callable: triage a roster's inbound offers across Instagram, TikTok and YouTube from Claude or any MCP client."
- "USD or INR, with an India-market mode, because a converted US rate isn't an Indian rate."
- "Built for creators and talent managers, not brands."

Low-usage Actors are hidden from Store search, so give judges the direct URL ([Apify blog](https://blog.apify.com/apify-store-search-update/)).

---

## 7. BVAL pay-per-event pricing: $0.99 per full deal

| Event | Price | Charged when |
|---|---|---|
| `apify-actor-start` | Platform default | Every run |
| `deal-evaluated` | **$0.79** | Scrape, line items, range and verdict are done for one creator × one offer |
| `counter-email-drafted` | **$0.20** | `generateEmail: true` and the email is returned |
| `manual-deal-evaluated` | **$0.25** | `manual_metrics` supplied, so there is no scrape (reprice with new terms) |

Use plain PPE: the "PPE + usage" toggle takes 14 days to apply. Turn off the synthetic per-item event. Apify keeps 20% ([monetization](https://docs.apify.com/actors/monetize), [PPE](https://docs.apify.com/actors/monetize/pay-per-event.md)).

**Margin per full deal at $0.99.** After Apify's 20%, each deal brings in **$0.79**. Feeder costs on the FREE tier:

| Platform | Feeder cost | Net per deal | Margin |
|---|---|---|---|
| Instagram | $0.082 | ~$0.67 | ~6× |
| TikTok | ~$0.09 | ~$0.66 | ~6× |
| YouTube | $0.12-0.24 | ~$0.51-0.63 | ~3-5× |

Net figures also subtract an LLM cost of about $0.01-0.03 per email and about $0.01 of compute. Both are assumptions to measure. If child-run charges land on the caller rather than BVAL (undocumented, see section 10), the margin rises further. One price across all platforms keeps the README simple. If YouTube margins matter, add a $0.15 `youtube-surcharge` event.

**Against competitors.** BVAL costs about half of hypebridge's ~$1.95 per handle, and hypebridge returns no verdict or email. It costs about 1/30 of NegotiRate's £25 report. A manager pricing 40 deals a month pays about $40.

---

## 8. Counter-offer email: structure, rules, red flags

**Prompt input.** Structured JSON only: creator, brand, platform, verdict, line items (label, price, end date, source), ask/fair/floor, red flags, two option bundles (full scope at ask; reduced scope with its price), one platform-appropriate proof point (IG: median Reel plays and ER; TikTok: median plays; YouTube: median views on videos 30+ days old), tone and currency.

**Outline** (150-250 words, readable on a phone), following [Beacons](https://beacons.ai/i/blog/how-to-reply-to-a-brand-deal-email) and [Elev8or](https://www.elev8or.io/blog/how-to-negotiate-brand-deals):

1. Thanks, plus one line showing the creator read the brief.
2. Fit, backed by the proof point.
3. An itemized quote, every line with a price and an end date. Usage: type, channels and days from the post date. Partnership/Spark Ads: days. Exclusivity: named category and window. YouTube: placement and links.
4. Pushback on each flagged term, each with one alternative (for example a 12-month license instead of perpetual, or 30 days plus renewals at X% per 30 days).
5. A two-option close: "Full scope at $A, or [reduced scope] at $B. Which works better on your side?"
6. Terms: 50% deposit, Net 30, rights effective on full payment.
7. A short sign-off.

**Rules for the LLM:**

- Use only numbers from the input JSON.
- Never lower the price without removing scope.
- Give every right an end date.
- Never grant usage or exclusivity for gifted product.
- Never accept perpetual or AI-training rights at the base price.
- Never reveal the floor or walk-away.
- Keep the tone friendly and collaborative.
- `DECLINE_OR_REDUCE_SCOPE`: decline warmly and offer the minimum scope ([Elev8or templates](https://www.elev8or.io/blog/brand-collaboration-email-templates-for-creators)).
- `ACCEPT`: confirm deliverables, dates, usage, exclusivity, fee, payment terms and revisions.

**Red flags detected from input terms:**

| Flag | Trigger | Basis |
|---|---|---|
| `PERPETUAL_RIGHTS` | `perpetual`, or usage over 365 days | "Broad, cheap, and forever" ([Net Influencer](https://www.netinfluencer.com/perpetuity-whitelisting-ai-clauses-23-creator-economy-experts-on-what-brands-get-wrong-about-creator-usage-rights/)) |
| `UNPRICED_WHITELISTING` | Partnership/Spark Ads requested, and offer below the price without them | "A distinct asset, not a free add-on" (same source) |
| `USAGE_OVERBUY` | Paid usage over 180 days on short-form | Assets peak in 4-6 weeks (same source) |
| `LONG_EXCLUSIVITY` | Exclusivity over 7 days, or `full` scope | 2-7 days is normal ([Modash](https://www.modash.io/blog/influencer-exclusivity)) |
| `GIFTED_FOR_RIGHTS` | Offer of 0 or product only, with usage or exclusivity | [Beacons](https://beacons.ai/i/blog/how-to-reply-to-a-brand-deal-email) |
| `AI_LIKENESS` | `ai_training_clause` | Strike it or price it separately ([Net Influencer](https://www.netinfluencer.com/perpetuity-whitelisting-ai-clauses-23-creator-economy-experts-on-what-brands-get-wrong-about-creator-usage-rights/)) |
| `SLOW_PAY_NO_DEPOSIT` | Payment terms over 60 days, or deposit under 50% | Net 90 with no deposit is a walk-away signal ([Elev8or](https://www.elev8or.io/blog/how-to-negotiate-brand-deals)) |
| `RUSH_UNPAID` | Rush under 72 hours, and offer below fair | Rush is +25-50% ([Influenceflow](https://influenceflow.io/resources/rate-cards-for-influencer-services-the-complete-2026-guide)) |
| `EXCESS_REVISIONS` | More than 2 revision rounds included | 1 round is standard ([Stack Influence](https://stackinfluence.com/blog/how-to-price-ugc-content-as-a-creator-rates-and-rights)) |
| `FREE_RAW_FOOTAGE` | Raw footage requested and unpriced | +20-30% ([IMH](https://influencermarketinghub.com/organic-vs-paid-usage-rights/)) |
| `BUNDLE_SQUEEZE` | 3 or more deliverables, and offer under 0.85 × discounted fair | 92% of marketers bundle ([Modash](https://www.modash.io/blog/bundling-influencer-negotiation)) |
| `NA_TERM` | A term in the platform's `not_applicable` list (for example Spark Ads on YouTube) | Config |
| `VAGUE_USAGE` | Usage with no duration or channels | [Elev8or](https://www.elev8or.io/blog/how-to-negotiate-brand-deals) |

---

## 9. Limitations, confidence and how to show uncertainty

**Sources disagree by 2-10×.**

- **Nano Reel prices:** IMH puts them at $20-100, while Aspire's median is $250.
- **Follower rule of thumb:** $10 per 1K followers versus $100 per 1K ([Buffer](https://buffer.com/resources/influencer-marketing-cost/) vs [Modash](https://www.modash.io/blog/influencer-pricing)).
- **One-year usage:** quoted anywhere from 75% to over 200% of base.
- **Whitelisting priced on ad spend:** 1-5% versus 5-20% ([Toptal](https://www.toptal.com/creator/post/usage-rights-for-creators) vs [impact.com](https://impact.com/influencer/how-much-to-charge-for-usage-rights-influencer/)).
- **Dedicated YouTube vs integration:** 1.7-2× versus 3-5×.
- **YouTube tier tables:** these blend integrations and dedicated videos, and impact.com's mid band ($9,000-25,000) is far above view-based estimates. That is why the clamp minimums are deliberately loose.

Nearly all of the data comes from vendor blogs, and the niche multipliers come from YouTube CPM tables but are applied to Reels and TikTok as well.

**Pure assumptions:**

- Floor and walk-away multipliers
- Clamp minimums
- Engagement curve
- TikTok ER bands (3%/9%) and YouTube ER bands (2%/5%)
- Shorts CPM and clamps
- YouTube comparable-age window (30-365 days)
- TikTok volatility flag
- Crowding factor of 1.25 (tempered from 1.5, because category midpoints already blend in difficult categories)
- Full exclusivity at 2×
- Link-in-bio, Story-sticker and pinned-comment fees
- Cross-posting fee
- Rush fee
- The 60-day and 180-day buckets
- TikTok follower fallback
- The claims that TikTok views decay fast and YouTube views accumulate for months

The India factors are derived from blog ranges, and India's macro tier (500K-2M) has different bounds from BVAL's.

**How BVAL shows uncertainty:**

1. Always return a range (walk-away / floor / fair / ask), never one price.
2. Return `confidence` (high / medium / low / very_low), based on valid sample size, which views field or age fallback was used, whether the clamp fired, whether likes were hidden, and TikTok volatility.
3. Attach `source_ids` and an `is_assumption` flag to every line item.
4. Return `data_used`: n, median views, ER, field, age window and scrape time.
5. Include a fixed disclaimer: "Benchmark-based estimate from public 2026 industry sources, not financial or legal advice. Rates vary 2-10× across sources; use as a negotiation anchor."
6. Return `rates_version`.

---

## 10. Open questions to settle in a live test run

1. Does the Reel scraper return a non-zero `videoPlayCount` for most Reels today? Compare against the app for 3 handles. Does the post scraper's `basicData` include `videoPlayCount`?
2. Does the end-to-end run finish in under 60 seconds per platform? No feeder publishes durations. Time the parallel IG pair, TikTok, YouTube with 30 or 60 items, and the LLM call.
3. Who pays for child runs, the caller or the developer? This is undocumented; test with a second account. YouTube's $0.24 makes this matter most.
4. What are the exact `Actor.call` keyword names (`timeout`, `memory_mbytes`, `max_total_charge_usd`) and the `Actor.charge` signature in the installed SDK?
5. Does `streamers/youtube-scraper` return `likes`, `commentsCount` and an absolute `date` for channel-listed videos, not only for direct video URLs? How often do 30 NEWEST videos contain at least 6 that are 30 days old or more?
6. Is `authorMeta.fans` populated for TikTok accounts with few videos? Do private accounts return `error` items?
7. How common is `likesCount = -1` among mid-tier IG accounts?
8. Calibration: price 5-10 creators per platform with known rates and check that fair value lands inside LeadDyno's bands without clamping. Pay particular attention to YouTube, where the bands are weakest.
9. India mode for TikTok: verify TikTok's availability in India, where it has been blocked since 2020. If it is unavailable, limit `market=india` to Instagram and YouTube.
10. FX: load `usd_inr` from config, with an optional refresh at run time.

---

## 11. References

| ID | Source |
|---|---|
| leaddyno | [LeadDyno, Influencer pricing 2026 (incl. Aspire data)](https://www.leaddyno.com/blog/influencer-pricing) |
| later2026 | [Later, Influencer pricing benchmarks 2026](https://later.com/blog/influencer-pricing-benchmarks-the-complete-2026-guide/) |
| imh_rates | [Influencer Marketing Hub, Influencer rates 2026](https://influencermarketinghub.com/influencer-rates/) |
| imh_ig | [IMH, Instagram influencer rates](https://influencermarketinghub.com/instagram-influencer-rates/) |
| imh_usage | [IMH, Organic vs paid usage rights](https://influencermarketinghub.com/organic-vs-paid-usage-rights/) |
| modash_cpm | [Modash, Influencer marketing CPM](https://www.modash.io/blog/influencer-marketing-cpm) |
| modash_pricing | [Modash, Influencer pricing](https://www.modash.io/blog/influencer-pricing) |
| modash_excl | [Modash, Influencer exclusivity](https://www.modash.io/blog/influencer-exclusivity) |
| modash_bundling | [Modash, Bundling in negotiation](https://www.modash.io/blog/bundling-influencer-negotiation) |
| iqfluence | [iQfluence, CPM in influencer marketing](https://iqfluence.io/public/blog/cpm-influencer-marketing) |
| tryspansa | [TrySpansa, Influencer rate card (Apr 2026)](https://dev.to/tryspansa/influencer-rate-card-what-brands-should-pay-43oj) |
| creatordb_aol | [CreatorDB via AOL, YouTube influencer costs](https://www.aol.com/2025-influencer-marketing-costs-youtube-133000232.html) |
| impact_yt | [impact.com, YouTube sponsorship rates](https://impact.com/?p=35983) |
| buffer_cost | [Buffer, Influencer marketing cost (incl. Lumanu per-view)](https://buffer.com/resources/influencer-marketing-cost/) |
| collabstr_pay | [Collabstr, Influencer pay](https://collabstr.com/blog/influencer-pay) |
| collabstr_2026 | [Collabstr, 2026 influencer marketing report](https://collabstr.com/2026-influencer-marketing-report) |
| hypeauditor_er | [HypeAuditor, Instagram ER calculator and benchmarks](https://hypeauditor.com/free-tools/instagram-engagement-calculator/) |
| hypeauditor_tt | [HypeAuditor, TikTok engagement rate](https://blog.hypeauditor.com/what-is-tiktok-engagement-rate-why-brands-should-take-note/) |
| dash_social | [Dash Social, H2 2025 benchmarks](https://pages.dashsocial.com/hubfs/social-media-benchmark/2025/H2/all-industry.pdf) |
| hootsuite | [Hootsuite, Influencer pricing](https://blog.hootsuite.com/influencer-pricing/) |
| upgrowth | [upGrowth, Influencer pricing India 2026](https://upgrowth.in/influencer-marketing-pricing-india-2026/) |
| grynow | [Grynow, Influencer marketing cost in India (Aug 2026)](https://www.grynow.in/blog/influencer-marketing-cost-in-india.html) |
| hdfc_fx_1 | [HDFC Sky, Rupee at 93.27 (18 Nov 2026)](https://hdfcsky.com/news/rupee-rises-24-paise-to-93-27-against-us-dollar-in-early-trade-november-18-2026) |
| hdfc_fx_2 | [HDFC Sky, Rupee closes at 94.20](https://hdfcsky.com/news/rupee-falls-8-paise-to-close-at-94-20-against-us-dollar) |
| toptal_usage | [Toptal, Usage rights for creators](https://www.toptal.com/creator/post/usage-rights-for-creators) |
| impact_usage | [impact.com, How much to charge for usage rights](https://impact.com/influencer/how-much-to-charge-for-usage-rights-influencer/) |
| netinf_33 | [Net Influencer, 33 professionals on perpetual usage](https://www.netinfluencer.com/one-fee-no-expiration-33-creator-economy-professionals-on-whether-perpetual-usage-rights-are-ever-a-fair-deal/) |
| netinf_23 | [Net Influencer, 23 experts on usage, whitelisting, AI](https://www.netinfluencer.com/perpetuity-whitelisting-ai-clauses-23-creator-economy-experts-on-what-brands-get-wrong-about-creator-usage-rights/) |
| stack | [Stack Influence, UGC pricing and rights](https://stackinfluence.com/blog/how-to-price-ugc-content-as-a-creator-rates-and-rights) |
| lumanu | [Lumanu, Whitelisting and usage fees](https://www.lumanu.com/blog/how-influencers-charge-whitelisting-usage-rights) |
| sozee_wl | [Sozee, Whitelisting rates guide (snippet)](https://sozee.ai/resources/influencer-whitelisting-rates-guide) |
| socialync | [Socialync, Whitelisting rates 2026 (snippet)](https://www.socialync.io/blog/whitelisting-rates-what-to-pay-creators-2026) |
| selene | [Selene the Lawyer, Rate card template](https://selenethelawyer.squarespace.com/blog/influencer-rate-card-template) |
| creatorsjet | [CreatorsJet, Influencer exclusivity (snippet)](https://www.creatorsjet.com/blog/influencer-exclusivity) |
| influenceflow | [Influenceflow, Rate cards 2026 (snippet)](https://influenceflow.io/resources/rate-cards-for-influencer-services-the-complete-2026-guide) |
| backstage | [Backstage, Influencer rate card (snippet)](https://backstage.com/magazine/article/how-to-create-an-influencer-rate-card-79713/) |
| templatenet | [Template.net, Influencer rate sheet (snippet)](https://www.template.net/edit-online/462510/influencer-rate-sheet) |
| elev8or | [Elev8or, How to negotiate brand deals](https://www.elev8or.io/blog/how-to-negotiate-brand-deals) |
| elev8or_email | [Elev8or, Brand collaboration email templates](https://www.elev8or.io/blog/brand-collaboration-email-templates-for-creators) |
| beacons | [Beacons, How to reply to a brand deal email](https://beacons.ai/i/blog/how-to-reply-to-a-brand-deal-email) |
| apify_ig | [instagram-reel-scraper](https://apify.com/apify/instagram-reel-scraper.md) ([API](https://api.apify.com/v2/acts/apify~instagram-reel-scraper), [schema](https://api.apify.com/v2/acts/apify~instagram-reel-scraper/builds/default)), [instagram-post-scraper](https://apify.com/apify/instagram-post-scraper.md), [instagram-profile-scraper](https://apify.com/apify/instagram-profile-scraper.md) ([API](https://api.apify.com/v2/acts/apify~instagram-profile-scraper)) |
| apify_tt | [clockworks/tiktok-profile-scraper](https://apify.com/clockworks/tiktok-profile-scraper.md) ([API](https://api.apify.com/v2/acts/clockworks~tiktok-profile-scraper)), [clockworks/tiktok-scraper API](https://api.apify.com/v2/acts/clockworks~tiktok-scraper) |
| apify_yt | [streamers/youtube-scraper](https://apify.com/streamers/youtube-scraper.md), [streamers/youtube-channel-scraper](https://apify.com/streamers/youtube-channel-scraper.md) |
| apify_sdk | [Apify Python SDK, Interacting with other Actors](https://docs.apify.com/sdk/python/docs/concepts/interacting-with-other-actors.md) |
| apify_ppe | [Apify monetization](https://docs.apify.com/actors/monetize), [Pay-per-event](https://docs.apify.com/actors/monetize/pay-per-event.md), [Store search update](https://blog.apify.com/apify-store-search-update/) |
| competitors | [hypebridge-pricing](https://apify.com/hypebridge/hypebridge-pricing), [kayhermes](https://apify.com/kayhermes/creator-sponsorship-rate-estimator), [apricot_blackberry](https://apify.com/apricot_blackberry/rate-card-generator), [zaver.api](https://apify.com/zaver.api/instagram-influencer-price-calculator), [trovevault](https://apify.com/trovevault/influencer-pricing-calculator), [HypeAuditor calculator](https://hypeauditor.com/free-tools/instagram-pricing-calculator/), [NegotiRate](https://www.producthunt.com/posts/1094453), [CreatorFlowX](https://www.producthunt.com/products/creatorflowx/makers), [Sovaio](https://www.producthunt.com/products/sovaio/reviews), [Collabstr](https://collabstr.com/influencer-price-calculator), [IMH calculator via Neal Schaffer](https://nealschaffer.com/instagram-influencer-calculators/), [Qoruz](https://qoruz.com/tools/influencer-cost-checker), [Elev8or India platforms](https://www.elev8or.io/blog/best-influencer-marketing-platforms-in-india) |
