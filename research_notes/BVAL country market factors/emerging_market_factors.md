# BVAL country market factors: Brazil, Mexico, Indonesia, Philippines, Japan (plus a short look at KSA, UAE and Turkey)

Research date: 2026-11-22. All factors are **relative to US** and are meant to multiply BVAL's US model output (US CPMs: Reels $20, TikTok $12, Shorts $8, YT integration $22).

**FX used (dated):**

| Currency | Units per USD | Date / basis | Source |
|---|---|---|---|
| BRL | 5.1298 | Oct-2026 monthly avg | [Fed G.5, 2026-11-02](https://www.federalreserve.gov/releases/g5/20261102/) |
| MXN | 18.4464 | Oct-2026 monthly avg | [Fed G.5, 2026-11-02](https://www.federalreserve.gov/releases/g5/20261102/) |
| JPY | 157.9748 | Oct-2026 monthly avg | [Fed G.5, 2026-11-02](https://www.federalreserve.gov/releases/g5/20261102/) |
| INR | 95.5167 | Oct-2026 monthly avg | [Fed G.5, 2026-11-02](https://www.federalreserve.gov/releases/g5/20261102/) |
| IDR | 18,255 | close 2026-11-19 | [Bisnis.com](https://market.bisnis.com/read/20261119/93/2022767/rupiah-ditutup-melemah-ke-rp18255-per-dolar-as-hari-ini-1911) |
| PHP | 62.87 | close 2026-10-14 (no Nov quote found) | [Inquirer](https://business.inquirer.net/617575/peso-breaches-63-61-level) |

**US reference prices used to compute the factors (assumption, labelled DERIVED):** nano $200, micro $800, mid $3,000, macro $7,500, mega $15,000 per Reel/TikTok-equivalent post. These are rough central values from wide, conflicting 2026 US/global guides: Later quotes $200–500 for nano Reels/TikToks ([Later](https://later.com/blog/influencer-pricing-benchmarks-the-complete-2026-guide/)), IMH quotes $100–500 for Instagram micro and $200–800 for TikTok micro ([IMH](https://influencermarketinghub.com/influencer-rates/)), ContentGrip quotes $800–5,000 for TikTok macro (100K–1M) ([ContentGrip](https://contentgrip.com/influencer-marketing-cost/)), and Impact's 2025 table is much higher (IG micro $2,000–8,000) ([Impact](https://impact.com/influencer/how-much-do-influencers-charge-per-post/)). **For the code, the best approach is to recompute each factor as (local USD price) ÷ (BVAL's own US price at that tier).** The local USD prices are listed below so you can do that.

Method: where a source gives a wide range, I take the **geometric midpoint** (sqrt(low×high)), because these ranges span 5–10x.

---

## Q1. Typical per-post prices in local currency by tier and platform (2025–2026)

### Takeaway
Japan has a structured, fairly transparent market. Per-follower pricing there is ¥2–4 for Instagram and ¥4–7 for video, and per-post prices come to about 0.5–0.75x US. Brazil and Indonesia have usable 2026 local-currency tables, which put them at about 0.1–0.6x US, with the factor rising with tier. For the Philippines I found peso figures only for nano and mega. For Mexico I found no credible MXN rate card for 2025–2026.

### Cited Findings

**Brazil (BRL; USD at 5.1298)**
- **Veeras survey of 1,330 BR creators (published 2026-03-03, updated 2026-10-14).** These are medians of the *starting* prices creators ask on Instagram:
  - 1K–5K followers: Feed R$100, Stories R$50, Reels R$150 ($29). The middle half of Reels asks runs R$100–250.
  - 5K–10K: Reels R$200 ($39). Middle half R$100–300.
  - 10K–50K: Feed R$150, Stories R$80, Reels R$200 ($39). Middle half R$140–300.
  - 50K–500K: Feed R$425, Stories R$150, Reels R$500 ($97). Middle half R$250–800.
  - Niche Reels medians: beauty/fashion/lifestyle R$150, fitness R$180, travel/sports R$200.
  - The page says no TikTok or YouTube price reference with a known sample exists.
  - Source: [Veeras](https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital)
- **Metricool estimates, quoted by Veeras (no sample stated):** R$15,000–25,000 per post for 100K–1M followers ($2,924–4,873), and R$80,000+ for 1M–7M followers ($15,600+). Source: [Veeras](https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital) citing [Metricool](https://metricool.com/pt/quanto-ganha-influenciador/)
- **A 2026 BR table, from a search summary of Brazilian blogs (inteligenciasetorial / agenciagram):**
  - Micro (5K–20K): R$300–600 per Reels ($58–117), R$100–200 per Stories.
  - Mid (20K–100K): R$600–1,500 per Reels ($117–292).
  - Macro (100K–500K): R$1,500–5,000 per Reels ($292–975).
  - Sources: [inteligenciasetorial](https://inteligenciasetorial.com.br/marketing/quanto-cobrar-por-publipost-no-tiktok/); [agenciagram](https://agenciagram.com.br/blog/como-ser-micro-influenciador-instagram-2026). Not verified by direct fetch.
- **Conflicting Veeras numbers in a search snippet:** nano R$100–500, micro (10–50K) R$500–2,500, macro (200K–1M) R$10K–50K. The fetched page did not show these figures, so they may come from an earlier version. Treat with caution. Source: [Veeras](https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital)
- **YOUPIX Creators & Negócios 2025 (income only, no per-post rates):**
  - 22.96% of BR creators earn up to R$2,000/month and 23.61% earn R$2,000–5,000.
  - About 12% earn more than R$10K/month.
  - 41% still live mainly from sponsored content.
  - Source: [Propmark](https://propmark.com.br/digital/metade-dos-creators-com-mais-de-tres-anos-de-carreira-ja-fatura-acima-de-r-10-mil-aponta-youpix/)

**Mexico (MXN; USD at 18.4464)**
- Cronoshare gives MXN 2,000–25,000 per post ($108–1,355), with no tier breakdown and no date. Source: [Cronoshare](https://www.cronoshare.com.mx/cuanto-cuesta/contratar-influencer)
- Mercately says local influencers charge "from a few thousand pesos" per post and gives no exact figure. Source: [Mercately](https://blog.mercately.com/es/cuanto-cobra-un-influencer-tarifas-actuales-y-factores-que-las-influyen)
- El Universal (undated) quotes USD figures: from $25 per post for nano (Facebook), from $250 for micro, and from $1,250 for mid-tier. Source: [El Universal](https://www.eluniversal.com.mx/cartera/dime-quien-anuncias-y-te-dire-que-influencer-eres/)
- One search-result guide claims "a Mexican micro-influencer might charge $500–1,200 for deliverables that cost $2,000–3,000 in the US." That implies 0.25–0.40x US. The exact page could not be pinned down; it appeared among the results for [CreatorsJet ES](https://www.creatorsjet.com/es/blog/tarifas-de-influencers-por-plataforma-y-numero-de-seguidores-basadas-en-12000-campanas), [InfluenceFlow](https://influenceflow.io/resources/influencer-pricing-benchmarks-2025-complete-guide-to-creator-rates-market-data/) and others. Unverified.
- Expansión (2026-10-13) confirms that no per-deal pricing data exists in Mexico. AVE, CiM and IAB México will only begin mapping influencer-marketing firms in 2027. Influencer spend sits inside an MXN 776M "other" category within an MXN 191,315M total ad market for 2025. Source: [Expansión](https://expansion.mx/mercadotecnia/2026/10/13/cuanto-dinero-llega-influencers-intermediacion-calculo)

**Indonesia (IDR; USD at 18,255)**
- **ContentGrip, "Influencer marketing in Indonesia: a 2026 brand guide" (2026-06-15).** Prices are per post or video in IDR. The first column is unlabelled and assumed to be Instagram. Source: [ContentGrip](https://contentgrip.com/influencer-marketing-indonesia/)

  | Tier (followers) | IG sponsored post | TikTok video |
  |---|---|---|
  | Nano 1K–10K | Rp200K–1M ($11–55) | Rp400K–2M ($22–110) |
  | Micro 10K–100K | Rp1M–10M ($55–548) | Rp2M–15M ($110–822) |
  | "Macro" 100K–500K | Rp10M–25M ($548–1,370) | Rp15M–50M ($822–2,739) |
  | "Mega" 500K–1M | Rp25M–80M ($1,370–4,382) | Rp50M–150M ($2,739–8,217) |

- TikTok is priced at roughly 1.5–2x Instagram at every tier in Indonesia ([ContentGrip](https://contentgrip.com/influencer-marketing-indonesia/)). This is the opposite of the US relationship in BVAL, where the TikTok CPM ($12) is below Reels ($20).
- Mediatics research (2023–24, older) puts TikTok *celebrity* endorsements at Rp7M–39.5M per video ($383–2,164). That is far below the ContentGrip mega range, so the two sources disagree. Sources: [Databoks/Katadata](https://databoks.katadata.co.id/index.php/en/media/statistics/a77cc6cdf9541fc/tiktok-celebrity-endorsement-rates-in-indonesia-starting-from-rp7-million-per-video); [GoodStats](https://data.goodstats.id/statistic/berapa-biaya-yang-harus-disiapkan-buat-endorse-seleb-tiktok-jQYyJ)
- Regional guide: a nano creator in Indonesia or Vietnam often makes a sponsored TikTok for under $200, and SEA micro creators typically cost $300–1,500 depending on platform. Source: [ContentGrip](https://contentgrip.com/influencer-marketing-cost/)
- Engagement: Instagram nano creators average about 7.2% versus 1.1% for creators above 100K, and TikTok nano creators have a median of 8.1%. Source: [ContentGrip](https://contentgrip.com/influencer-marketing-indonesia/)

**Philippines (PHP; USD at 62.87)**
- **Spiralytics (page updated 2026-06-25), citing DMSM's "2025 Philippines Influencer Rate Guide":**
  - Nano (1K–10K): ₱1,000–5,000 per post ($16–80).
  - Mega (1M+): from ₱150,000 ($2,386).
  - No micro, mid or macro figures and no platform split.
  - Source: [Spiralytics](https://www.spiralytics.com/blog/influencer-marketing-philippines)
- Elev8or (a creator directory, method unknown) gives micro at ₱14,408–86,445 per post ($229–1,375). This is far above the DMSM-implied curve, so I treat it as low reliability. Source: [Elev8or](https://www.elev8or.io/find/tiktok-fashion-influencers-in-philippines)

**Japan (JPY; USD at 157.97)**
- **TaTap (published 2026-11-17).** Per-post prices, excluding tax. Source: [TaTap](https://tatap.jp/knowledge/influencer-marketing-costs/)
  - Nano (1K–10K): ¥10K–50K ($63–317)
  - Micro (10K–100K): ¥30K–150K ($190–950)
  - Middle (100K–500K): ¥150K–800K ($950–5,064)
  - Mega (500K–1M): ¥500K–1.5M ($3,165–9,495)
  - Top (1M+): ¥1M–3M+ ($6,330–18,990+)
  - Platform order: YouTube is highest, then Reels above static posts. TikTok is about the same as Instagram, and X is low.
- **Follower unit price (フォロワー単価):** ¥2–4 per follower is the common guide ([TaTap X article](https://tatap.jp/knowledge/x-influencer-marketing-costs/)). Another agency gives ¥2–7 overall: Instagram feed ¥2–4, and YouTube/TikTok with video production ¥4–7 ([atsoho](https://atsoho.com/blog/micro-influencer-marketing-agency-rate); [atsoho PR単価](https://atsoho.com/blog/influencer-pr-tanka)).
- **YouTube tie-ups (タイアップ):** about ¥1.5–4 per subscriber, so a 100K-subscriber channel runs ¥150K–400K ($950–2,532). Another formula is past-30-day average views × ¥2–10 (stated as December 2025 data), which equals a CPM of ¥2,000–10,000 ($12.7–63). Sources: [imitsu](https://imitsu.jp/cost/movie/youtuber-request); [media-radar](https://media-radar.jp/mediapicks/article/knowledge/columns4-youtuber_cost). These came via a search summary, and I could not tell which page gave which formula.
- CyberBuzz is cited as forecasting that the JP influencer market will reach about ¥100B in 2026 (via a search summary of [s--line](https://s--line.co.jp/influencer-marketing/)).

**India (no change):** I did not find a better 2026 source. Keep the existing factors (nano 0.20, micro 0.25, mid 0.40, macro/mega 0.55).

### Inferences
- Brazil's survey medians from Veeras are creator-side *asking floors* on a self-serve platform, and they sit below agency or brand-side figures. Brand-paid prices are better represented by the blog tables plus the Metricool estimates. The Veeras numbers are useful as a lower bound only.
- In Japan, per-follower pricing at ¥3 × 50K = ¥150K ($950) for a mid-micro creator is roughly at US level. Japan is the only country in this set close to parity.

### Gaps
- No tiered BRL rates for TikTok or YouTube with a known sample. Veeras states explicitly that none exists.
- No MXN tiered rate card for 2025–2026 from a credible local agency or study. Mexico is the weakest country in this set.
- No PHP micro, mid or macro rates, and no YouTube rates for Indonesia or the Philippines.
- Could not reach Squid, Airfluencers, BR Media, AnyMind, Partipost, SociaBuzz, Allstars, CyberBuzz or UUUM rate pages within the time budget. The influee.co/pt page returned 403.

---

## Q2. CPM and cost-per-view benchmarks by country, and published geo factors

### Takeaway
YouTube ad-CPM ratios to the US are a usable proxy for *direction*, but they understate influencer prices by about 2–7x. India's YouTube CPM ratio is about 0.08 while its accepted influencer factors are 0.20–0.55. Japan's ad CPM ratio is 0.29, yet its influencer prices are close to US level. The only creator CPM found is Brazil's: R$15–35 per 1K views, which is $2.9–6.8, or about 0.15–0.34x BVAL's $20 US Reels CPM.

### Cited Findings
- **YouTube median CPM by country.** Data from IsThisChannelMonetized, covering videos uploaded in 2024; medians; countries with fewer than 1,000 views excluded. Reported by [Digital Information World, 2025-08-11](https://www.digitalinformationworld.com/2025/08/youtube-cpm-rates-in-2025-how-location.html). The ratio column is DERIVED.

  | Country | YT CPM (USD) | Ratio to US |
  |---|---|---|
  | US | 11.95 | 1.00 |
  | Japan | 3.41 | 0.29 |
  | UAE | 3.03 | 0.25 |
  | Saudi Arabia | 2.18 | 0.18 |
  | Mexico | 1.64 | 0.14 |
  | Brazil | 1.33 | 0.11 |
  | Philippines | 1.22 | 0.10 |
  | India | 0.96 | 0.08 |
  | Indonesia | 0.87 | 0.07 |
  | Turkey | 0.87 | 0.07 |

- Other datasets disagree on levels but agree on ordering. Japan comes in at about $2.93–5.68, Brazil about $0.80–3, Mexico about $1.30–1.64, Indonesia about $0.30–1, and the Philippines about $0.30–1.22. Outlier lists show Brazil at $7.32, Mexico at $10.46 and Japan at $11.58. Sources: [Awisee](https://awisee.com/blog/youtube-cpm-rates); [thesrzone](https://www.thesrzone.com/2021/07/youtube-cpm-and-cpc-rates-by-country.html)
- **Brazil creator CPM:** average R$15–35 per 1,000 views (Veeras search snippet). The fetched page only gives an example: a CPM of R$20 on a Reel with 120K views = R$2,400. Source: [Veeras](https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital)
- **Japan YouTube tie-up implied CPM:** ¥2,000–10,000 per 1K views ($12.7–63), against a US integration CPM of $22 in BVAL. Sources: [imitsu](https://imitsu.jp/cost/movie/youtuber-request); [media-radar](https://media-radar.jp/mediapicks/article/knowledge/columns4-youtuber_cost)
- No published influencer geo-factor tables from TrySpansa, Modash, HypeAuditor, Collabstr or Kolsquare surfaced in this session.

### Inferences
- Rough empirical multiplier: influencer factor ≈ 2.5–5x the YouTube ad-CPM ratio for emerging markets. India: 0.08 → 0.20–0.55. Brazil: 0.11 → about 0.2–0.5 from rate cards. Japan breaks this pattern, with a ratio of 0.29 but influencer prices of about 0.7–1.0x, because of high per-follower pricing norms and agency-heavy deals.
- Mexico's YouTube CPM is slightly above Brazil's, which supports giving Mexico factors at or slightly above Brazil's in the absence of MXN rate cards.

### Gaps
- No country-level *influencer* (not ad) CPM benchmarks for MX, ID, PH or JP Reels/TikTok.
- No Shorts-specific country data.

---

## Q3. Local add-on norms, deal structure, payment and agency commission

### Takeaway
Usage rights, paid-ads whitelisting and exclusivity are priced as extras in all markets that have data. In Brazil, extras can double the base price. Japan has formal disclosure law (since October 2023) and agency fees of 20–30%, and secondary-use licences are often priced per case. Indonesia invoices in IDR and treats whitelisting or dark posting as a separate, priced right. For Mexico and the Philippines, I found no sourced add-on norms.

### Cited Findings
- **Brazil:**
  - Extras such as usage rights, multi-video packages and exclusivity can double the price.
  - Example: a 15K-follower creator with 8% engagement can charge R$600 for one Reels with 3-month usage rights ([inteligenciasetorial](https://inteligenciasetorial.com.br/marketing/quanto-cobrar-por-publipost-no-tiktok/), via search summary).
  - Veeras says these extras raise the price but gives no percentages ([Veeras](https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital)).
- **Indonesia:**
  - Creators invoice in IDR.
  - Whitelisting or dark posting for paid ads must be named in the contract and "priced as an extra right." Organic terms do not cover paid amplification.
  - Source: [ContentGrip](https://contentgrip.com/influencer-marketing-indonesia/)
- **Japan:**
  - Casting agency fee is 20–30% of the creator fee, or a fixed monthly fee. A direction fee is sometimes billed separately.
  - Agency outsourcing costs ¥200K–500K per month plus creator fees. Ambassador contracts run ¥100K–500K per month.
  - Secondary use (二次利用) is billed per case or as a percentage. TaTap charges ¥2,000 per case.
  - Gifting costs ¥8,000 per shipment request.
  - Stealth-marketing rules (景品表示法 amendment, effective October 2023): "PR" or "広告" labels are required when a fee is paid, when product is given with a posting request, or when content is specified.
  - Source: [TaTap](https://tatap.jp/knowledge/influencer-marketing-costs/)
- Another JP example adds 30% of the creator fee as a direction fee on top. Source: [atsoho](https://atsoho.com/blog/influencer-marketing-cost) (via search summary)
- **Global or regional:** creators who drive conversions increasingly structure deals as base rate plus CPA or revenue share. Source: [ContentGrip rate card](https://contentgrip.com/influencer-marketing-rate-card/)

### Inferences
- For BVAL, the add-on multipliers (usage rights, whitelisting/Spark/Partnership Ads, exclusivity) can reasonably stay global in percentage terms. Applied to a lower base, they produce lower absolute add-on prices. Brazil's "up to 2x with extras" is consistent with typical US practice.
- For Japan, consider adding a default agency/direction uplift of about 20–30% if BVAL quotes brand-side all-in prices.

### Gaps
- No sourced information on Brazil's CONAR #publi rules, BR payment terms (nota fiscal, net days) or BR agency commission.
- No sourced information on Mexico's PROFECO rules, SAT/factura practice, payment terms or agency commission. Expansión notes only an opaque chain of intermediaries.
- No information on Philippine disclosure or payment norms.
- No country-specific Spark Ads or Partnership Ads premiums.

---

## Q4. Derived market factor vs US by tier (feeds code)

### Takeaway
The proposed DERIVED midpoint factors are listed below. Japan sits close to US level, at about 0.7–0.75. Brazil and Mexico are India-like, at about 0.2–0.55. Indonesia and the Philippines are lowest, at about 0.15–0.45. Confidence is medium for Japan, Brazil and Indonesia, and low for Mexico and the Philippines.

### Cited Findings
These are the local-USD inputs, with geometric midpoints in parentheses, all from the sources in Q1.
- **Brazil:**
  - Nano: R$100–500 = $19.5–97 (geo $44) ([Veeras](https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital)).
  - Micro: R$300–2,500 = $58–487 (geo $168) ([inteligenciasetorial](https://inteligenciasetorial.com.br/marketing/quanto-cobrar-por-publipost-no-tiktok/); Veeras snippet).
  - Mid: R$1,500–25,000 = $292–4,873 (geo $1,193). This combines the blog macro range with Metricool's 100K–1M range.
  - Macro: R$10K–25K = $1,950–4,873 (geo $3,083).
  - Mega: R$80K+ = $15.6K+ ([Veeras/Metricool](https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital)).
- **Indonesia** ([ContentGrip](https://contentgrip.com/influencer-marketing-indonesia/)):
  - IG geo midpoints: nano $25, micro $174, 100–500K $866, 500K–1M $2,450.
  - TikTok geo midpoints: nano $49, micro $301, 100–500K $1,500, 500K–1M $4,744.
- **Philippines** ([Spiralytics/DMSM](https://www.spiralytics.com/blog/influencer-marketing-philippines)): nano $16–80 (geo $36); mega floor $2,386.
- **Japan** ([TaTap](https://tatap.jp/knowledge/influencer-marketing-costs/)): nano geo $142, micro $425, mid $2,193, mega (500K–1M) $5,482, 1M+ $10,965.
- **Mexico:** micro $500–1,200 against US $2,000–3,000, which implies 0.25–0.40 (unverified search-result guide). The YouTube CPM ratio is 0.14 ([DIW](https://www.digitalinformationworld.com/2025/08/youtube-cpm-rates-in-2025-how-location.html)).

### Inferences

**Raw ratios (geo midpoint ÷ US reference of nano $200, micro $800, mid $3,000, macro $7,500, mega $15,000):**

| Country | Nano | Micro | Mid | Macro | Mega |
|---|---|---|---|---|---|
| Brazil | 0.22 | 0.21 | 0.40 | 0.41 | ~1.0 (celebrity; unreliable) |
| Indonesia IG | 0.12 | 0.22 | 0.29 | 0.33 (500K–1M) | n/a |
| Indonesia TikTok | 0.25 | 0.38 | 0.50 | 0.63 (500K–1M) | n/a |
| Philippines | 0.18 | n/a | n/a | n/a | ≥0.16 (floor) |
| Japan | 0.71 | 0.53 | 0.73 | 0.73 | 0.73 |
| Mexico | n/a | 0.25–0.40 | n/a | n/a | n/a |

**PROPOSED BVAL factors (DERIVED midpoints, all platforms unless noted):**

| Country | Nano | Micro | Mid | Macro | Mega | Confidence |
|---|---|---|---|---|---|---|
| India (existing) | 0.20 | 0.25 | 0.40 | 0.55 | 0.55 | (existing) |
| Brazil | 0.20 | 0.25 | 0.38 | 0.50 | 0.55 | medium |
| Mexico | 0.22 | 0.30 | 0.40 | 0.50 | 0.55 | low (CPM ratio and one guide claim only) |
| Indonesia | 0.15 | 0.25 | 0.35 | 0.40 | 0.45 | medium |
| Philippines | 0.15 | 0.20 | 0.25 | 0.30 | 0.30 | low |
| Japan | 0.70 | 0.70 | 0.75 | 0.75 | 0.75 | medium |
| Saudi Arabia | 0.40 | 0.45 | 0.50 | 0.55 | 0.60 | very low (CPM ratio 0.18 only) |
| UAE | 0.50 | 0.55 | 0.60 | 0.65 | 0.70 | very low (CPM ratio 0.25 only) |
| Turkey | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | very low (CPM ratio 0.07 only) |

**Optional platform adjustments (DERIVED):**
- **Indonesia TikTok ×1.6** relative to the table, because TikTok prices are about 1.5–2x Instagram locally. This is clearly evidenced in ContentGrip.
- **Japan YouTube integration ≈ 1.0** (not 0.75), based on the implied tie-up CPM of ¥2,000–10,000 per 1K views ($28 geo) versus the US $22.
- **Brazil YouTube** has no data, so keep the base factor.

**Notes on the factor shape:**
- In emerging markets, factors rise with tier. Small creators' rates track local wages. Top creators sell to multinational brands with regional budgets.
- Japan is flat at about 0.7, set by per-follower pricing norms.

**Why some raw ratios were not used directly:**
- The Brazil mega raw ratio (~1.0) relies on a single Metricool "R$80K+ for 1M–7M" figure that mixes in celebrities, so 0.55 is capped to match India.
- The Brazil micro raw ratio (0.21) is pulled down by the Veeras creator-ask floors, so 0.25 is used.
- **Saudi Arabia, UAE and Turkey:** I found no rate cards. Their factors are placeholders that scale the YouTube CPM ratio by the Japan/India pattern, and the Gulf is assumed to price closer to the US. They should not ship without a source, or should ship flagged "estimated."

### Gaps
- The US reference prices are my central assumption from conflicting US guides. Recompute the factors against BVAL's own US per-tier outputs; the local USD inputs above make that mechanical.
- Factors depend on FX. BRL, IDR and PHP weakened materially in 2026: PHP went from ₱57.66 in February to about ₱63 in October ([Inquirer](https://business.inquirer.net/617575/peso-breaches-63-61-level)). Local-currency rate cards lag FX, so USD factors may drift down by about 5–10% if rate cards are not repriced.
- No Saudi Arabia, UAE or Turkey rate-card data was collected.
- 1M+ tier data exists only for Japan (TaTap). The other countries' mega factors are extrapolated.
