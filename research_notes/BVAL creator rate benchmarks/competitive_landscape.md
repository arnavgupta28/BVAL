# Competitive landscape: creator rate / sponsorship pricing tools (for BVAL), as of 22 Nov 2026

Method note: web tools were checked through vendor pages, Product Hunt and reviews. The Apify Store was queried on 2026-11-22 via `https://api.apify.com/v2/store?search=<term>&limit=50`, using 13 terms: influencer, creator rate, influencer pricing, engagement rate, influencer earnings, sponsorship, brand deal, media kit, influencer audit, creator valuation, youtube earnings, tiktok earnings and rate card. Results were filtered to valuation, pricing, audit and earnings Actors, and the closest competitors' READMEs were read through `apify.com/<actor>.md`. The store list API returns no `modifiedAt`, so "last modified" comes from `api.apify.com/v2/acts/<id>` for the closest competitors and from `lastRunStartedAt` for the rest.

## 1. Web rate calculators and creator tools: what they cover

### Takeaway
Most web calculators price one post from followers and engagement rate (ER), with no deal terms and no negotiation output. A few now take usage rights, whitelisting and exclusivity as inputs: HypeAuditor's free calculator, Direct.me, and several Apify Actors (section 3). Three 2026 consumer apps already judge a brand's offer and write a counter reply: NegotiRate, CreatorFlowX and Sovaio. None of them has a public API, so "offer verdict + counter email" is not new in itself. What is new is doing it inside one callable API/agent tool, with priced line items and a floor/ask/walk-away range.

### Cited Findings
**Free follower/ER calculators (no deal terms, no negotiation)**
- Influencer Marketing Hub calculator: inputs are follower count, ER and average likes per post. Output is one per-post price range (example: $92 to $154). No usage rights or whitelisting — [Neal Schaffer test](https://nealschaffer.com/instagram-influencer-calculators/)
- IMH also sells or distributes an "Influencer Rate & Campaign Budget Calculator" ebook/spreadsheet, which is a template rather than an automated tool — [IMH](https://influencermarketinghub.com/resources/ebooks/the-influencer-rate-campaign-budget-calculator/)
- inBeat shut down its free tools, and its calculator now redirects to a shutdown notice. Klear's calculator sits behind a premium trial — [Neal Schaffer](https://nealschaffer.com/instagram-influencer-calculators/)
- Collabstr: inputs are platform, niche and follower range. Output is the average rate of matching creators, drawn from more than 1.1M content packages listed on its marketplace (listed asking prices, not closed deals). No usage, whitelisting or counter — [Collabstr](https://collabstr.com/influencer-price-calculator)
- Upfluence Instagram pricing tool: input is a username, and it factors in past brand deals and fake-follower percentage — [Upfluence](https://www.upfluence.com/instagram-pricing/), summarized in [search via Neal Schaffer/others](https://nealschaffer.com/instagram-influencer-calculators/)
- Kolsquare "Kolculator" (input is a handle), Infloo (followers, ER, audience country; prices feed posts, Reels and Stories), Heepsy and Favikon (B2B, gives a confidence level) are all free one-post estimators — [Kolsquare](https://www.kolsquare.com/en/kolculator), [Infloo](https://infloo.io/en/influencer-price-calculator), [Heepsy](https://heepsy.com/free-tools/instagram-pricing-calculator), [Favikon](https://www.favikon.com/pt/free-tools/influencer-price-calculator)

**Free calculators that do take deal terms**
- HypeAuditor Instagram Pricing Calculator: inputs are format (Post/Reel/Story/Live), followers, ER (advanced), sponsor size, usage rights duration (none/3m/6m/1y/indefinite), whitelisting (yes/no), direct CTA, and exclusivity duration. Output is one per-post price range. It does not use views, has no niche field in the form, and has no counter-offer. It is free, and HypeAuditor sells a separate API — [HypeAuditor](https://hypeauditor.com/free-tools/instagram-pricing-calculator/)
- Direct.me brand-deal pricing calculator covers posts, Reels, TikTok, YouTube integrations, UGC, usage rights and exclusivity, and calls its output an "educational estimate" — [Direct.me](https://direct.me/tools/brand-deal-pricing-calculator)
- Inro calculator example: a $500 base plus 90-day organic reuse, paid and whitelisting, and 90-day category exclusivity comes to $1,000 — [Inro](https://www.inro.social/tools/influencer-pricing-calculator)
- Top Growth Marketing: formula based on views, CTR, conversion, average order value (AOV) and margin, with exclusivity as a separate monthly line — [TGM](https://topgrowthmarketing.com/?p=48924)

**Rate checks based on the creator's own data**
- Fohr Rate Check: inputs are your handle, what you usually charge, and the number of deliverables. Output is a "fair" rate based on impressions delivered rather than followers, adjusted for niche and partnership frequency. Usage and exclusivity are left as manual advice in the FAQ, whitelisting is not mentioned, there is no counter feature, and price is not stated — [Fohr](https://www.fohr.co/rate-check/creator)
- Beacons: media kit with rate cards plus a pricing calculator "built on real creator deal data", with base rates set from platform, media type and follower count. It also has a talent-manager product — [Beacons media kit](https://beacons.ai/i/app-pages/media-kit), [Beacons for managers](https://beacons.ai/i/for-managers), [Beacons calculator (now redirects to blog)](https://home.beacons.ai/app-pages/pricing-calculator)
- Passionfroot: creator storefront with a media kit and set-your-own-rates. A "Sponsorship Pricing Guide" is referenced, but no automated rate engine was found — [Passionfroot](https://passionfroot.me/creators)
- FYPM: crowdsourced brand-deal pay database (vendor-claimed figure of more than 100k creators, unverified). The free tier is limited, and full access needs a paid subscription plus contributing your own deals. It sells a benchmark report (2023: 16,000 deals, 7,200 brands), and a 2026 "Rate Calculator Beta" and "Creator Deal Index" were mentioned — [creatoreconomytools](https://creatoreconomytools.com/tool/f-you-pay-me), [Lindsey Gamble](https://www.lindseygamble.com/blog/fypm-releases-2023-creator-pricing-benchmark-report), [FYPM newsletter](https://fypm-newsletter.beehiiv.com/p/a-fair-deal-shouldn-t-be-this-hard)

**Direct competitors on concept: offer verdict and counter reply (consumer web apps, 2026)**
- NegotiRate (negotirate.app, UK, launched 2026): inputs are platform (TT/IG/YT/UGC), audience, views, engagement, niche, deliverables, usage terms and the brand's offer. The free output is an underpayment % and the £ gap. A £25 report adds a counter-offer email, negotiation scripts and a red-flag clause scanner. No API mentioned, and usage, whitelisting and exclusivity are not priced as separate line items — [Product Hunt](https://www.producthunt.com/posts/1094453)
- CreatorFlowX (launched 2026, about 6 months ago): rates an offer weak/fair/strong from views, engagement, niche pricing, deliverables, exclusivity and platform ("not follower count alone"), and generates counter replies. Usage rights are not mentioned, price is not listed, and there is no API — [Product Hunt](https://www.producthunt.com/products/creatorflowx/makers)
- Sovaio (YouTube only, free, 2026): the creator uploads YouTube Studio analytics and gets a rate card, offer evaluation and draft replies. Usage and exclusivity are not mentioned, and there is no API — [Product Hunt](https://www.producthunt.com/products/sovaio/reviews)
- Adjacent: Snippet ("AI talent manager" for mid-tier creators: discovery, outreach, negotiation, contract review) — [Microlaunch](https://microlaunch.net/h/how-to-automate-sponsorship-outreach-and-negotiation-processes). CreatorBiz.ai is a Gmail extension that summarizes deal terms and flags risks but is not built around counter emails — [Chrome Web Store](https://chromewebstore.google.com/detail/creatorbizai-—-ai-deal-as/fnahdapjmcmiphfhfcihkcdpoekgigal)

**Enterprise influencer platforms (brand-side; not creator pricing tools)**
- Modash: from $99/mo annual or $120/mo monthly (Modash's own blog), while G2 lists $299/mo, so the sources conflict. API listed as a feature — [G2](https://www.g2.com/products/modash/pricing), [Software Advice](https://www.softwareadvice.com/influencer-marketing/modash-profile)
- Upfluence: from $478/mo for one search-and-contact module (G2), annual contracts — [G2](https://www.g2.com/products/upfluence/pricing)
- GRIN: no public pricing, annual contracts, no free trial. Its API is for e-commerce integration — [Modash blog (competitor source)](https://www.modash.io/it/blog/grin-alternatives)
- Later Influence: "contact vendor" — [Capterra](https://capterra.com/compare/162056-195693/Upfluence-vs-Modash)
- Influencity: has a "casting call" negotiation workflow inside the platform where brands and creators exchange offers (a messaging and offer flow, not a fair-rate engine) — [Influencity KB](https://knowledge.influencity.com/casting-call/how-to-negotiate-in-influencity-for-creators)
- Favikon notes that API access is a hidden cost across these platforms — [Favikon](https://www.favikon.com/blog/influencer-marketing-platform-pricing)

**Market pricing conventions (useful for BVAL's add-on logic and README claims)**
- Usage rights add roughly 20–50% of base. Whitelisting is priced as a % of base per 30 days or as a % of ad spend. Exclusivity adds 25–50% and should be quoted as its own line, separate from paid usage — [Lumanu](https://www.lumanu.com/blog/how-influencers-charge-whitelisting-usage-rights), [impact.com](https://impact.com/influencer/how-much-to-charge-for-usage-rights-influencer/), [IMH organic vs paid usage](https://influencermarketinghub.com/organic-vs-paid-usage-rights/)

### Inferences
- The field splits into three groups. (a) Free one-post estimators (follower/ER), which are commoditized and in some cases being shut down. (b) Rate cards with term multipliers (HypeAuditor, Direct.me, Beacons). (c) Consumer "is this offer fair + counter email" apps (NegotiRate, CreatorFlowX, Sovaio). BVAL should not claim it is the first counter-offer generator. It can claim to combine all three in one API call, built on scraped real view data.
- None of the group (c) apps shows itemized pricing for usage, whitelisting/Spark ads and exclusivity together with a floor/ask/walk-away range. NegotiRate gives a gap %, and CreatorFlowX gives a weak/fair/strong label. No product found handles Spark Ads or partnership-ad codes explicitly.
- No creator-side tool found offers an API, MCP or agent endpoint. Talent managers pricing many deals across a roster have to use web UIs one deal at a time.

### Gaps
- Not verified individually (no time or no results): Social Blade (its earnings formula), Later, Hootsuite, NeoReach, Stan, Linktree, Kajabi calculators, Clear Influence and Creator Wizard. Searches for "Creator Wizard" and "Clear Influence" returned nothing relevant. Social Blade's earnings estimates are YouTube ad revenue, not sponsorship rates (inferred from the Apify Social Blade scraper descriptions in section 3).
- NegotiRate, CreatorFlowX and Sovaio were assessed only from Product Hunt pages. Their accuracy, actual inputs and usage numbers are unknown.
- The current price of the Beacons and Passionfroot paid tiers was not confirmed.

## 2. Indian tools offering rate estimates

### Takeaway
Indian platforms (Kofluence, Winkl, Plixxo) sell managed campaigns with pricing on request. No public INR rate calculator was found for them. Qoruz has a handle-based "influencer cost checker" that likely quotes in INR. None of them prices usage, whitelisting or exclusivity, or writes counter-offers, so the Indian creator and manager segment is underserved.

### Cited Findings
- Kofluence: "pricing on request, managed campaigns". Clutch lists a minimum project of $10k+ — [Elev8or](https://www.elev8or.io/blog/best-influencer-marketing-platforms-in-india), [Clutch](https://clutch.co/profile/kofluence)
- Qoruz: discovery and tracking, free tier, paid plans reportedly from about ₹15,000/mo — [Elev8or](https://www.elev8or.io/blog/best-influencer-marketing-platforms-in-india); G2 lists no official pricing — [G2](https://www.g2.com/products/qoruz/pricing)
- Qoruz influencer cost checker: input is an Instagram handle and the output is an "influencer cost". The page shows rupee icons, so INR is likely but not confirmed. It does not mention usage, exclusivity or whitelisting, and has no counter feature (the FAQ says to negotiate directly) — [Qoruz](https://qoruz.com/tools/influencer-cost-checker)
- Winkl and Plixxo: no published pricing or rate tool found. Plixxo is described as a beauty/fashion/lifestyle network that is part of POPxo — [echai.ventures](https://echai.ventures/d2c/r/winkl-influencer-marketing-ecosystem--r-winkl-platform)
- Other India benchmark sources are content guides rather than tools: Upgrowth (Instagram earnings calculator), Ticktime (INR rate card and CPV calculator), Superprofile and Bosswallah guides. Benchmarks conflict: for a 100k creator, one source says ₹60k–2L per Reel and another says ₹15k–50k per post — [Ticktime](https://ticktime.media/blogs/influencer-rate-card-india-2026-instagram-reel-story-youtube-video-pricing), [Superprofile](https://superprofile.bio/guides/influencer-rate-card-india), [Bosswallah](https://bosswallah.com/blog/brand-collaborations/micro-influencer-rates-in-india-what-to-actually-charge-in-2026/), [Upgrowth](https://upgrowth.in/?p=51298)

### Inferences
- An INR-aware BVAL (currency plus India CPM benchmarks) would face almost no tool competition. The wide spread in published INR benchmarks supports pricing from views rather than followers.

### Gaps
- No Kofluence, Winkl or Plixxo pages surfaced for a self-serve rate estimator. They may exist behind sign-up.

## 3. Apify Store landscape (queried 2026-11-22)

### Takeaway
The Store has many creator scrapers, plus a long tail of very low-usage (0–2 monthly users) pricing Actors, mostly published Feb–Oct 2026. Two already price usage, whitelisting and exclusivity add-ons: hypebridge/hypebridge-pricing and kayhermes/creator-sponsorship-rate-estimator. A third (apricot_blackberry/rate-card-generator) returns usage and exclusivity multipliers. None of the top-50 results for 13 search terms takes the brand's offer as input, returns a verdict, gives a floor/ask/walk-away range, or writes a counter-offer email. The search for "counter offer" and "walk away" text across all 13 result sets found zero matches. The category has no demand leader: the best pricing Actor has 2 monthly users.

### Cited Findings
**Closest competitors (pricing and rate cards)**

| Actor | Monthly users (30d) / total | Pricing | Created / modified | What it outputs | Usage / whitelist / exclusivity | Offer verdict / counter |
|---|---|---|---|---|---|---|
| [hypebridge/hypebridge-pricing](https://apify.com/hypebridge/hypebridge-pricing) | 1 / 2 | PPE: about $0.25 per pricing report plus $1.70 per influencer evaluation when starting from a handle ("from $0.167" with discounts) | 2026-10-03 / 2026-11-11 | IG/TikTok rate card (dedicated video, static, carousel, story, story x3, UGC) with [low, high] and an anchor; `commercialScenarios` for 30/90/365-day usage, 30-day whitelisting, 30-day exclusivity and a package; niche, ER and geo multipliers; JoinBrands UGC comps; past partnerships. A new handle takes 2–3 minutes | Yes, at fixed durations only | No. Pitched for "sanity-check an inbound quote" but takes no offer input and gives no email |
| [kayhermes/creator-sponsorship-rate-estimator](https://apify.com/kayhermes/creator-sponsorship-rate-estimator) | 2 / 3 | $5 per 1,000 estimates | 2026-07-14 / 2026-07-25 | Low/mid/high, CPM, confidence, assumptions, HTML report. You supply the metrics (followers, avgViews, ER, geo, deliverables); it does not scrape | Yes: usageRightsMonths, paidMediaUsage, exclusivityMonths, whitelisting, turnaround | No |
| [apricot_blackberry/rate-card-generator](https://apify.com/apricot_blackberry/rate-card-generator) | 0 / 4 | $15 per 1,000 cards | 2026-02-07 / 2026-11-13 | YT/IG/TT low/mid/high per format, cited CPM sources, authenticity adjustment | Usage (+20–30%) and exclusivity (+15–25%) as separate multipliers; no whitelisting | No. README says "not a fair price" |
| [zaver.api/instagram-influencer-price-calculator](https://apify.com/zaver.api/instagram-influencer-price-calculator) | 1 / 2 | $79.90 per 1,000 | 2026-10-02 / 2026-10-16 | Fair USD range for one IG reel, CPM, 0–100 score, authenticity | Explicitly excludes them ("negotiated separately") | No |
| [trovevault/influencer-pricing-calculator](https://apify.com/trovevault/influencer-pricing-calculator) | 1 / 13 | PPE | 2026-03-27 / 2026-10-24 | Formula bands (±20%) across 8 platforms from user-entered followers, ER, niche and country; optional views | Explicitly excluded | No |
| [centorprat/instagram-influencer-audit](https://apify.com/centorprat/instagram-influencer-audit) (+ [YouTube](https://apify.com/centorprat/youtube-influencer-audit), [TikTok](https://apify.com/centorprat/tiktok-influencer-audit) variants) | 1 / 2 (YT 1, TT 0) | $0.05 per audit (+$0.05 for deep forensics) | last run 2026-11-21 | Fake-follower signals, tier ER benchmark, brand safety, CPM rate-card estimate | No | No |
| [salomon.labs/youtube-channel-analyzer](https://apify.com/salomon.labs/youtube-channel-analyzer) | 1 / 2 | $30 per 1,000 | last run 2026-11-20 | Expected views, audience language, sponsor history, price from your own CPM | No | No |
| [moggedhq/youtube-earnings-estimator](https://apify.com/moggedhq/youtube-earnings-estimator) | 2 | $0.02 per channel | last run 2026-11-20 | Ad earnings range, niche RPM, "sponsorship value" | No | No |
| [hypebridge/influencer-evaluation-agent-instagram-tiktok](https://apify.com/hypebridge/influencer-evaluation-agent-instagram-tiktok) | 13 | $0.20 per item | last run 2026-11-20 | AI influencer evaluation (feeds hypebridge-pricing) | n/a | No |

Sources for the table: Apify Store API search results (stats, pricing, `lastRunStartedAt`), `api.apify.com/v2/acts/<id>` (created/modified), and each Actor's `.md` README, linked in the table.

**Other low-usage Actors that also estimate prices** (all 0–1 monthly users): [vant47/instagram-influencer-audit](https://apify.com/vant47/instagram-influencer-audit) (ER, fake-follower risk, earnings estimate, $0.04 each); [vant47/youtube-influencer-engagement-rate](https://apify.com/vant47/youtube-influencer-engagement-rate) (adds a sponsor price); [yugenox/instagram-creator-analytics](https://apify.com/yugenox/instagram-creator-analytics) (median plays, sponsored vs organic, price estimate); [apricot_blackberry/instagram-creator-analyzer](https://apify.com/apricot_blackberry/instagram-creator-analyzer) (per-post sponsorship estimate, $0.08); [funny_ground/tiktok-influencer-audit](https://apify.com/funny_ground/tiktok-influencer-audit) (sponsored-video rate estimates); [orbitai/creator-sponsorship-fit-scorer](https://apify.com/orbitai/creator-sponsorship-fit-scorer) ("likely campaign value"); [buseta/tiktok-scraper](https://apify.com/buseta/tiktok-scraper) (AI creator audit for brand deals, 3 monthly users) — Apify Store API

**Adjacent categories with real demand (inputs BVAL could chain, or substitutes)**
- Profile scrapers: [apidojo/tiktok-profile-scraper](https://apify.com/apidojo/tiktok-profile-scraper) (1,084 monthly users; "perfect for … brand deals"), [khadinakbar/tiktok-profile-scraper](https://apify.com/khadinakbar/tiktok-profile-scraper) (111, 0–80 Influencer Score), [apidojo/instagram-scraper-api](https://apify.com/apidojo/instagram-scraper-api) (443) — Apify Store API
- Social Blade earnings scrapers (YouTube ad-earnings estimates, not sponsorship rates): [radeance/socialblade-api](https://apify.com/radeance/socialblade-api) (34), [solidcode/socialblade-scraper](https://apify.com/solidcode/socialblade-scraper) (24), [dami_studio/socialblade-scraper](https://apify.com/dami_studio/socialblade-scraper) (11), plus about 10 clones with 1–2 users each — Apify Store API
- Engagement-rate and fake-follower vetting (about 20 Actors, 1–8 users each), e.g. [seemuapps/instagram-fake-follower-auditor](https://apify.com/seemuapps/instagram-fake-follower-auditor) (8, $0.99 per audit), [memo23/tiktok-fake-followers-checker](https://apify.com/memo23/tiktok-fake-followers-checker) (3, $0.30 per audit), [nerolabs/engagement-rate-checker](https://apify.com/nerolabs/engagement-rate-checker) (markets itself as "Agent-ready: MCP, x402") — Apify Store API
- Sponsor detection (which brands pay which creators): [transparent_meteorite/youtube-sponsorship-tracker](https://apify.com/transparent_meteorite/youtube-sponsorship-tracker) (6), [seemuapps/youtube-sponsorship-tracker](https://apify.com/seemuapps/youtube-sponsorship-tracker) (5), [gganbukim/youtube-sponsorship-finder](https://apify.com/gganbukim/youtube-sponsorship-finder) (2) — Apify Store API
- Chinese marketplace rate cards (official quoted prices and CPM from Xingtu, Pugongying and Huahuo): [atomus/douyin-scraper](https://apify.com/atomus/douyin-scraper) (575, includes Xingtu rate cards), [zen-studio/douyin-xingtu-rankings-scraper](https://apify.com/zen-studio/douyin-xingtu-rankings-scraper) (11), [memo23/xiaohongshu-kol-scraper](https://apify.com/memo23/xiaohongshu-kol-scraper) (3) — Apify Store API. These are real transaction-style benchmarks, but for China only.
- CPM benchmarks: [fayoussef/whop-clipping-campaigns-scraper](https://apify.com/fayoussef/whop-clipping-campaigns-scraper) (26; reward per 1K views on Whop clipping campaigns), [hamsmoothie/newsletter-rate-card-extractor](https://apify.com/hamsmoothie/newsletter-rate-card-extractor) — Apify Store API
- Media kit: no Western media-kit generator found. [afkdigital/creator-partnership-profile-analyzer](https://apify.com/afkdigital/creator-partnership-profile-analyzer) reads existing media kits (1 user) — Apify Store API
- Negotiation pattern from another domain: [danielmichalek/freelance-proposal-writer](https://apify.com/danielmichalek/freelance-proposal-writer) gives a GO/MAYBE/SKIP verdict with a price inside your rate card plus a written proposal, which is the same output shape as BVAL but for freelancers — Apify Store API

### Inferences
- Demand in this category sits in scrapers (hundreds to 1,000+ monthly users) and not in the pricing layer (0–2 monthly users each). Pricing Actors are a crowded, unproven long tail. BVAL should position as a deal-decision tool, not as "another rate calculator".
- hypebridge-pricing is the strongest technical overlap (handle in, priced usage, whitelisting and exclusivity scenarios). It is still brand-oriented: fixed 30/90/365-day scenarios, no offer input, no verdict, no counter text, 2–3 minutes per new handle, about $1.95 per handle. kayhermes covers term inputs but needs metrics supplied by the user.
- Every pricing Actor calls itself "a planning estimate, not a quote". None turns its estimate into a decision (accept, counter or walk) or a message ready to send.

### Gaps
- `modifiedAt` was not available from the store list endpoint. Created and modified dates were fetched only for the top 5 competitors.
- Only the top 50 results per term were scanned. The `total` counts (for example 13,109 for "rate card") are fuzzy matches, mostly unrelated scrapers.
- Actor output quality and accuracy were not tested by running the Actors.

## 4. The remaining gap and BVAL's differentiation

### Takeaway
No single tool, web or Apify, does all of the following. It takes the brand's actual offer and terms. It prices each term (usage by duration and paid vs organic, whitelisting/Spark/partnership-ad codes, exclusivity by scope and duration) as line items on a base built from the creator's real recent views. It returns floor/ask/walk-away figures and a verdict. It drafts the counter email. And it does all this as an API or agent-callable endpoint. The pieces exist separately: priced add-ons (HypeAuditor, hypebridge, kayhermes), offer verdict plus counter (NegotiRate, CreatorFlowX, Sovaio), and view-based fair rate (Fohr, zaver). Nobody combines them.

### Cited Findings
- Offer, verdict and counter tools exist only as consumer web apps with no API mentioned: NegotiRate (£25 per report), CreatorFlowX and Sovaio (YouTube only) — [NegotiRate PH](https://www.producthunt.com/posts/1094453), [CreatorFlowX PH](https://www.producthunt.com/products/creatorflowx/makers), [Sovaio PH](https://www.producthunt.com/products/sovaio/reviews)
- The Apify pricing Actors with term add-ons return rate cards or scenarios but take no offer and produce no negotiation output — [hypebridge-pricing](https://apify.com/hypebridge/hypebridge-pricing), [kayhermes](https://apify.com/kayhermes/creator-sponsorship-rate-estimator), [apricot_blackberry](https://apify.com/apricot_blackberry/rate-card-generator)
- Several Actors explicitly exclude usage, exclusivity and whitelisting from their price — [zaver.api](https://apify.com/zaver.api/instagram-influencer-price-calculator), [trovevault](https://apify.com/trovevault/influencer-pricing-calculator)
- HypeAuditor's calculator takes usage, whitelisting and exclusivity, but prices from followers and ER (not views) and has no offer or counter — [HypeAuditor](https://hypeauditor.com/free-tools/instagram-pricing-calculator/)
- Industry guidance says usage, whitelisting and exclusivity should be separate line items, which BVAL's itemized output does — [Lumanu](https://www.lumanu.com/blog/how-influencers-charge-whitelisting-usage-rights), [IMH](https://influencermarketinghub.com/organic-vs-paid-usage-rights/)

### Inferences (suggested README / demo claims)
- Lead with "the brand's offer in, the decision out": verdict, floor/ask/walk-away, and a counter email that cites the line items. This is the one combination no Apify Actor has, and the consumer apps that do it are not API-callable.
- "Priced from views, not followers." Scrape the last N posts' median views (via the Apify scrapers that already have demand) and price CPM on real reach. This sets BVAL apart from IMH, Collabstr, HypeAuditor, Beacons and zaver, which are follower- or ER-based.
- "Every term is a line item with a reason": usage by duration and organic vs paid, whitelisting/Spark Ads/partnership ads per 30 days, exclusivity by category scope and duration. hypebridge offers only fixed 30-day whitelisting and exclusivity scenarios. Spark/partnership-ad codes are not named by any tool found.
- "Agent-callable": an Actor plus the Apify MCP, so a talent manager's agent can triage a roster's inbound offers in bulk. That is a gap against every web tool listed, and good fodder for the demo (for example, paste 5 inbound brand emails and get 5 verdicts and counters).
- Buyer angle: hypebridge and zaver pitch to brands ("what to pay"), while BVAL takes the creator and manager side ("what to ask, when to walk"). An INR mode would add an India angle that no Indian platform covers with a self-serve tool.
- Honest framing: do not claim to be the first counter-offer tool (NegotiRate and CreatorFlowX exist). Claim to be the first API/agent-callable one, and the only one that itemizes terms on top of real view data.

### Gaps
- No usage or traction data for NegotiRate, CreatorFlowX or Sovaio, so their market validation is unknown.
- Whether any enterprise platform (CreatorIQ, Grin, Later) has an internal "suggested rate" feature with deal terms could not be verified, because their pricing and features are behind demos.
