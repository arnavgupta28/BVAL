# Price any country from one US engine

BVAL should keep one USD engine and add a `markets` block that changes only four things per country: a per-tier price factor, a few platform multipliers, which platforms are allowed, and how the result is shown (currency, rounding, tax label, ad-disclosure line, email language). Name eight countries explicitly: **US, India, UK, Germany, Brazil, Indonesia, Mexico and Canada**. Together they take at least **57% of global creator spend**, and they include all four of the largest Instagram/TikTok/YouTube audiences. Every other country falls into one of **12 regional groups plus a catch-all**, and only China is refused. Factors run from **0.15 (Indonesian nano creators) to 0.95 (UK and Canadian mega creators)** against the US. Developed English-speaking markets sit near US parity. Germany is around 0.8. Brazil, Mexico, India and Indonesia start at 0.15–0.22 for small creators and rise to about 0.55 at the top, because large creators sell to multinational brands with regional budgets. India keeps its existing factors (0.20/0.25/0.40/0.55/0.55). One correction matters for the code: Indonesia's "TikTok about 1.6× Instagram" premium has to become **×2.0 on BVAL's TikTok unit**, because BVAL's US TikTok CPM is already only 0.6× the Reel CPM. No public dataset gives price by country, tier and platform, so every factor is derived and carries a confidence level and its sources. The JSON in this report can be merged as written.

## Eight named markets carry the spend and the audiences

Two rankings pull in different directions. On money spent with creators, the US takes **43% of global creator spend**, followed by the UK at 5%, Germany at 4%, Brazil, France and Canada at 2% each, and India and Australia at 1% each. India is the fastest-growing market, forecast at +20% for 2026, out of a global total of **$116B** ([Madison and Wall via Net Influencer](https://www.netinfluencer.com/advertiser-spending-on-creators-to-reach-116b-usd-in-2026-report-shows/)). On audience size, India (515M Instagram plus 573M YouTube ad reach), the US, Indonesia (240M on TikTok, the largest TikTok audience anywhere) and Brazil lead, with Mexico next ([DataReportal IG](https://datareportal.com/essential-instagram-stats), [TikTok](https://datareportal.com/essential-tiktok-stats), [YouTube](https://datareportal.com/essential-youtube-stats)). Only the US, India, Brazil and the UK rank high on both. Germany is the third-largest spend market. Indonesia and Mexico bring large numbers of creators who might use the tool, even though brands there spend little. Canada adds 2% of spend for almost no work: it is English-speaking and its currency and market sit close to the US.

France, Australia and Japan just miss the cut. Australia and France fit their groups closely: the Tier-1 English group factor is 0.80–0.90 against Australia's derived 0.80–0.90, and the Western Europe group is 0.65–0.75 against France's derived 0.62–0.70. Japan does not fit its group. Agency-heavy, per-follower pricing (¥2–4 per follower) puts Japan at **about 0.70–0.75 of US**, with YouTube near parity ([TaTap](https://tatap.jp/knowledge/influencer-marketing-costs/)). Its group, Developed East Asia, also holds Singapore at about 0.30 and Korea and Taiwan with ad CPMs at roughly 0.43 of the US. Japan should be the first country promoted to a named entry. Promoting a country means adding one object under `countries`, with no change to code.

## Factors run from 0.15 to 0.95, and rise with creator size in emerging markets

The developed-market factors blend three inputs: **50% Kolect's transactional price per 1K views** (120K+ deals, mostly 2026), **25% InfluencerFee's country index**, and **25% YouTube ad-CPM ratios** as a measure of audience value. Kolect is weighted most because BVAL also prices off views. On that measure the UK sits at 0.97× US, Germany at 0.92×, France at 0.78× and Canada at 1.19× ([Kolect](https://www.kolect.ai/guides/influencer-rates), [Kolect CPM 2026](https://www.kolect.ai/reports/influencer-cpm-benchmarks-2026)). InfluencerFee, which describes its numbers as "generated algorithmically", puts every market 10–40% below the US ([InfluencerFee](https://influencerfee.com/blog/influencer-pricing-by-country/)). YouTube ad CPMs put the UK, Canada and Germany at only 0.54–0.68× ([DIW](https://www.digitalinformationworld.com/2025/08/youtube-cpm-rates-in-2025-how-location.html), [MilX](https://milx.app/trends/which-countries-have-the-best-youtube-cpm-rates-in-2025)). Canada is the weakest of these blends, at 1.19× from Kolect against 0.70× from InfluencerFee. It ships at 0.90 with low confidence.

The emerging-market factors come from local-currency rate cards converted at dated FX. For Brazil these are 2026 blog tables, a survey of 1,330 creators' asking prices from Veeras, and Metricool estimates ([Veeras](https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital), [inteligenciasetorial](https://inteligenciasetorial.com.br/marketing/quanto-cobrar-por-publipost-no-tiktok/)). For Indonesia it is ContentGrip's June 2026 IDR table ([ContentGrip](https://contentgrip.com/influencer-marketing-indonesia/)). Mexico has no credible MXN rate card. Expansión reports that no per-deal data will exist until an industry mapping in 2027 ([Expansión](https://expansion.mx/mercadotecnia/2026/10/13/cuanto-dinero-llega-influencers-intermediacion-calculo)). Mexico's factors therefore rest on its YouTube CPM, which is slightly above Brazil's, and carry low confidence. The rising curve in these markets is deliberate. Small creators charge rates that track local wages, while top creators sell to multinational brands with regional budgets.

| Market | Nano | Micro | Mid | Macro | Mega | Platform multiplier | Confidence |
|---|---|---|---|---|---|---|---|
| US | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | none | high |
| India | 0.20 | 0.25 | 0.40 | 0.55 | 0.55 | TikTok unavailable | medium |
| UK | 0.80 | 0.85 | 0.85 | 0.90 | 0.95 | TikTok ×0.95 | medium |
| Germany | 0.75 | 0.80 | 0.80 | 0.80 | 0.85 | TikTok ×0.90 | low |
| Brazil | 0.20 | 0.25 | 0.38 | 0.50 | 0.55 | none | medium |
| Indonesia | 0.15 | 0.25 | 0.35 | 0.40 | 0.45 | **TikTok ×2.0** | medium (TikTok: low) |
| Mexico | 0.22 | 0.30 | 0.40 | 0.50 | 0.55 | none | low |
| Canada | 0.85 | 0.90 | 0.90 | 0.95 | 0.95 | TikTok ×0.95 | low |

**India reconciles cleanly.** The new research found no better 2026 source than the one behind the existing factors, and the factors agree with InfluencerFee's India index of 15–30. They therefore stay as they are. They move from `currency.india_market_factor_by_tier` into `markets.countries.IN.factor_by_tier`, and `niche_multipliers.india_overrides` moves into `countries.IN.niche_overrides`. The INR rate stays at **93.5**, the mid-November spot ([HDFC Sky](https://hdfcsky.com/news/rupee-rises-24-paise-to-93-27-against-us-dollar-in-early-trade-november-18-2026)). The Fed's October average of 95.52 ([Fed G.5](https://www.federalreserve.gov/releases/g5/20261102/)) is older, and the 2% gap between them is within normal refresh noise.

**Platform multipliers mean different things depending on the source.** InfluencerFee indexes each platform against the *same* US platform, so the UK/Canada TikTok ×0.95 and Germany TikTok ×0.90 (5–10 index points below Instagram) apply directly. Kolect's UK medians point the other way, so ×1.0 is also defensible for the UK. ContentGrip's Indonesian premium works differently: it compares TikTok with Instagram *within* Indonesia, at 1.5–2× per post at every tier. BVAL's US TikTok unit uses a $12 CPM against $20 for Reels (0.6×). A ×1.6 multiplier would therefore price an Indonesian TikTok slightly *below* an Indonesian Reel at the same views, which inverts the local market. The true conversion is 1.6 ÷ 0.6 ≈ 2.7. That figure is tempered to **2.0** for two reasons: view-based pricing already rewards TikTok's larger reach there, and InfluencerFee's Southeast Asia index puts TikTok *below* Instagram. As a check, Example B's mid-tier TikTok base of $1,260 becomes **$882** (0.35 × 2.0), inside ContentGrip's Indonesian mid-tier range of $822–2,739. At ×1.6 it would be $706, below that range. Japan's YouTube ≈1.0 (a tie-up CPM of about $28 geometric midpoint against the US $22) waits until Japan is named.

## Thirteen fallback groups give every other country a factor

Any ISO code that is not named maps to a group, and any code not listed anywhere goes to `rest_of_world`. Where a group lacks rate cards, its factor scales the YouTube ad-CPM ratio up by the pattern seen in India and Brazil: influencer prices run about **2.5–5× higher than ad-CPM ratios suggest**. For example, India's CPM ratio of 0.08 sits against factors of 0.20–0.55 ([DIW](https://www.digitalinformationworld.com/2025/08/youtube-cpm-rates-in-2025-how-location.html), [YTMoneyCalculator](https://ytmoneycalculator.com/blog/youtube-cpm-rates-by-country/)). Group factors are deliberately coarse, and every group outside the first four is `very_low` or `low` confidence.

| Group | Main members | Nano → Mega | Basis |
|---|---|---|---|
| tier1_english | AU, NZ, IE (+JE, GG, IM) | 0.80 → 0.90 | Kolect AU 0.89 per view, InfluencerFee AU 75 |
| western_europe | FR, NL, BE, AT, CH, Nordics | 0.65 → 0.75 | France derived 0.62–0.70, lifted for NL/CH/Nordics |
| southern_europe | ES, IT, PT, GR, IL | 0.52 → 0.62 | Kolect ES 0.67 / IT 0.63 per view, ×0.9 |
| eastern_europe | PL, CZ, RO, HU, UA, Baltics | 0.20 → 0.35 | CPM ratio 0.12–0.25, scaled up |
| turkiye_central_asia | TR, KZ, UZ, Caucasus, MN | 0.15 → 0.35 | Turkey CPM ratio 0.07–0.12 |
| latin_america | AR, CO, CL, PE, Caribbean | 0.18 → 0.45 | Just below BR/MX (CPM 0.08–0.11 vs 0.12–0.14) |
| south_asia | PK, BD, LK, NP | 0.15 → 0.40 | India × ~0.7 (CPM $1.00 vs $1.50) |
| southeast_asia | PH, VN, TH, MY | 0.15 → 0.30 | Philippines DMSM nano/mega, InfluencerFee SEA 10–25 |
| east_asia_developed | JP, KR, TW, HK, SG | 0.60 → 0.65 | Japan 0.70–0.75, SG ~0.30, KR/TW CPM ~0.43 |
| gulf | AE, SA, QA, KW, BH, OM | 0.50 → 0.65 | UAE 55–70 index; Saudi CPM sources differ ~3× |
| mena_other | EG, MA, DZ, JO, IQ | 0.12 → 0.30 | Egypt CPM ratio ~0.06 |
| sub_saharan_africa | NG, ZA, KE, GH | 0.12 → 0.30 | CPM ratio 0.08–0.18 |
| rest_of_world | Pacific islands, any unlisted code | 0.15 → 0.35 | assumption |

China is the only `unsupported` code. Instagram, YouTube and international TikTok are unavailable there, and ByteDance runs Douyin as a separate app ([DataReportal](https://datareportal.com/essential-tiktok-stats)). Hong Kong and Macau have their own ISO codes and stay in the East Asia group. Russia and Belarus sit in Eastern Europe, but no source covered them.

## The engine needs five practical rules per market

**Resolution and arithmetic.** Normalise `market` (uppercase, apply the aliases `UK`→`GB` and `GLOBAL`→`US`). Then look it up in this order: `unsupported` (return an error), `countries`, group `members`, and finally `rest_of_world`. Compute `f = factor_by_tier[tier] × platform_multipliers[platform]`. Apply `f` to the clamped unit price, so the clamp works in US terms and the factor comes after it. Apply the same `f` to the three fixed USD minimums: exclusivity $200, extra revision round $150, and whitelisting $100 per 30 days. Percentage add-ons then scale automatically, which fits the evidence that usage, whitelisting and exclusivity norms are not clearly different outside the US. German buyouts are quoted at 25–200% of the fee ([Kolsquare DE](https://www.kolsquare.com/de/blog/wie-viel-kostet-influencer-marketing-im-jahr-2025)), and Brazilian extras "can double" the price, both of which match US practice. Return `market_resolved: {code, matched: "country"|"group"|"catch_all", group_id, factor, confidence, fx_as_of}` so the user can see when a group fallback set the price. The `market` input means the *audience's* main country, not where the creator lives, because buyers price audience geography ([InfluencerFee](https://influencerfee.com/blog/influencer-pricing-by-country/)).

```python
def resolve(market, platform, tier, M):
    code = M["aliases"].get(market.upper(), market.upper())
    if code in M["unsupported"]: raise MarketError(M["unsupported_reason"][code])
    c = M["countries"].get(code)
    g = None if c else next((k for k, v in M["groups"].items() if code in v["members"]), "rest_of_world")
    src = c or M["groups"][g]
    if c and platform in c["unavailable_platforms"]: raise PlatformUnavailable(code, platform)
    pm = (c or {}).get("platform_multipliers", {}).get(platform) or 1.0
    return src["factor_by_tier"][tier] * pm, code, g, src
```

**Currency, FX and rounding.** The engine computes and returns USD by default. `output_currency: "LOCAL"` converts using the country's `fx_per_usd`, or for a group member its `member_currency` from the `fx` table. If neither exists, the output stays in USD. Every FX value carries a date and a source: the Fed G.5 October-2026 averages for most currencies ([Fed G.5](https://www.federalreserve.gov/releases/g5/20261102/)), IDR 18,255 at the 19 November close ([Bisnis.com](https://market.bisnis.com/read/20261119/93/2022767/rupiah-ditutup-melemah-ke-rp18255-per-dolar-as-hari-ini-1911)), and PHP 62.87 from 14 October ([Inquirer](https://business.inquirer.net/617575/peso-breaches-63-61-level)). A live refresh is optional, and the dated values are the fallback. Rounding applies after conversion. Named countries carry an explicit step (₹500, Rp100,000, MX$100, R$50, 10 for GBP/EUR/CAD/USD). Other currencies use the largest 1-2-5 step at or below 10 × `fx_per_usd`, which gives ¥1,000 and ₩10,000. Format INR with Indian grouping (₹2,61,000) and IDR in "Rp 12,7 juta" style.

**Tax.** Every price is ex-tax. Show the label, but add a tax line only when the input `creator_tax_registered` is true. The rates are India GST 18%, with reverse charge when a foreign creator bills an Indian brand ([Taxmann](https://www.taxmann.com/post/blog/opinion-impact-of-gst-on-social-media-influencers/)); UK VAT 20%, Germany 19% and Canada's federal GST 5% plus a provincial tax that varies ([VATupdate](https://www.vatupdate.com/2026/07/25/global-vat-rates-by-country-2026-standard-and-reduced-rates/)); and Indonesia PPN 12% ([PwC](https://taxsummaries.pwc.com/quick-charts/value-added-tax-vat-rates)). Mexico's IVA (16%) is unverified. Brazil's tax rate is left null because a dual-VAT reform is phasing in until 2033 ([KPMG](https://kpmg.com/kpmg-us/content/dam/kpmg/taxnewsflash/pdf/2026/digitalized-economy-taxation-developments-summary.pdf)).

**Platform availability.** TikTok is still blocked in India. The government denied unblocking reports in August 2025 and repeated that in February 2026 ([Business Today](https://www.businesstoday.in/india/story/no-comeback-for-tiktok-indian-govt-refutes-reports-of-ban-being-lifted-on-chinese-apps-490769-2025-08-23), [Patrika](https://www.patrika.com/en/national-news/tiktok-ban-in-india-not-lifted-says-modi-government-19886142)). `market=IN` with `platform=tiktok` must therefore return an error. In the US, TikTok has been fully available under the USDS Joint Venture since 22–23 January 2026 ([MacRumors](https://www.macrumors.com/2026/01/23/tiktok-avoids-us-ban-deal-officially-closes/)). Indonesia bars social platforms from processing payments, so shoppable posts must go through TikTok Shop or Tokopedia ([Asia Pacific Foundation](https://www.asiapacific.ca/publication/indonesias-new-e-commerce-regulations-take-bite-out-tiktoks)). A brief that asks for in-app checkout outside those channels should raise a red flag.

**Worked check.** In worked example A (Instagram micro, US fair price $2,793, with no fixed minimum binding), the market factor flows through like this:

| Market | Factor | Fair (USD) | Local display |
|---|---|---|---|
| GB | 0.85 | $2,374 | £1,790 + VAT |
| CA | 0.90 | $2,514 | C$3,550 + applicable taxes |
| DE | 0.80 | $2,234 | €2,000 zzgl. MwSt. |
| MX | 0.30 | $838 | MX$15,500 + IVA |
| IN / BR | 0.25 | $698 | ₹65,500 + GST / R$3,600 |
| ID | 0.25 | $698 | Rp12.700.000 |

## Merge-ready `markets` block for rates.json

Merge the block below at the top level of `rates.json`, then delete `currency.usd_inr`, `currency.india_market_factor_by_tier`, `currency.india_gst_pct` and `niche_multipliers.india_overrides`, and set `currency.rounding` to come from the market. `"assumption"` marks values that are BVAL's own judgment. Fields not in the original sketch are additive: `aliases`, `apply`, `selection_sources`, `fx_as_of`/`fx_source`, `notes`, `niche_overrides`, group `member_currency`/`email_language`, `unsupported_reason` and `fx`.

```json
{
  "markets": {
    "version": "2026-11-22.1",
    "default": "GLOBAL",
    "selection_sources": ["madison_wall", "datareportal_ig", "datareportal_tt", "datareportal_yt"],
    "aliases": { "GLOBAL": "US", "UK": "GB" },
    "apply": {
      "effective_factor": "factor_by_tier[tier] * platform_multipliers[platform]",
      "applies_to": ["clamped_unit_usd", "addons.exclusivity_min_usd", "addons.revisions.extra_round_min_usd", "addons.whitelisting_min_usd_per_30d"],
      "order": "clamp in US terms -> multiply by effective_factor -> package discount -> add-ons as % of content_base -> price points -> convert -> round",
      "quote_basis": "ex_tax",
      "rounding_rule_converted": "largest 1-2-5 step <= 10 * fx_per_usd (e.g. JPY 1000, KRW 10000, EUR 5)",
      "fx_refresh": "optional live refresh at run time; fall back to the dated values here and return fx_as_of"
    },
    "countries": {
      "US": {
        "name": "United States",
        "currency": "USD",
        "fx_per_usd": 1,
        "fx_as_of": null,
        "fx_source": null,
        "rounding": 10,
        "tax": { "name": "Sales tax", "pct": null, "note": "Creator services generally carry no sales tax; not verified per state. No tax line." },
        "factor_by_tier": { "nano": 1.0, "micro": 1.0, "mid": 1.0, "macro": 1.0, "mega": 1.0 },
        "platform_multipliers": { "instagram": 1.0, "tiktok": 1.0, "youtube": 1.0, "youtube_short": 1.0 },
        "unavailable_platforms": [],
        "disclosure": "FTC: clear, prominent disclosure of any material connection (e.g. #ad or the platform's Paid partnership label), not buried in hashtags.",
        "email_language": "en-US",
        "confidence": "high",
        "notes": "TikTok operates via the TikTok USDS Joint Venture since 22-23 Jan 2026.",
        "sources": ["leaddyno", "later2026", "nyu_jipel", "macrumors_tt"]
      },
      "IN": {
        "name": "India",
        "currency": "INR",
        "fx_per_usd": 93.5,
        "fx_as_of": "2026-11-18",
        "fx_source": "hdfc_fx_1",
        "rounding": 500,
        "tax": {
          "name": "GST",
          "pct": 18,
          "note": "Quote ex-GST ('+ 18% GST'); add the line only if the creator is GST-registered. A foreign creator billing an Indian brand: the brand pays GST under reverse charge."
        },
        "factor_by_tier": { "nano": 0.2, "micro": 0.25, "mid": 0.4, "macro": 0.55, "mega": 0.55 },
        "platform_multipliers": { "instagram": 1.0, "tiktok": null, "youtube": 1.0, "youtube_short": 1.0 },
        "unavailable_platforms": ["tiktok"],
        "disclosure": "ASCI: label chosen only from Advertisement, Ad, Sponsored, Collaboration, Partnership, Employee, Free gift, or Instagram Paid Partnership; not buried in hashtags; videos <=15s without caption need an on-screen label for >=3s.",
        "email_language": "en-IN",
        "niche_overrides": { "beauty": 1.2 },
        "confidence": "medium",
        "notes": "TikTok blocked since June 2020 under IT Act s.69A; reject platform=tiktok. Fed G.5 Oct-2026 average was 95.5167 INR/USD; 93.5 is the newer mid-Nov spot.",
        "sources": ["grynow", "upgrowth", "leaddyno", "tryspansa", "influencerfee", "hdfc_fx_1", "hdfc_fx_2", "fed_g5", "taxmann", "taxaj", "asci_pdf", "asci_dos", "businesstoday_tt", "techcrunch_tt", "patrika_tt"]
      },
      "GB": {
        "name": "United Kingdom",
        "currency": "GBP",
        "fx_per_usd": 0.7523,
        "fx_as_of": "2026-10 (monthly avg)",
        "fx_source": "fed_g5",
        "rounding": 10,
        "tax": {
          "name": "VAT",
          "pct": 20,
          "note": "Quote '+ VAT'; add the line only if the creator is VAT-registered (registration threshold not verified here)."
        },
        "factor_by_tier": { "nano": 0.8, "micro": 0.85, "mid": 0.85, "macro": 0.9, "mega": 0.95 },
        "platform_multipliers": { "instagram": 1.0, "tiktok": 0.95, "youtube": 1.0, "youtube_short": 1.0 },
        "unavailable_platforms": [],
        "disclosure": "ASA/CAP + CMA (guide updated Oct 2026): upfront #ad / #advert / #advertisement; 'Supported by', 'Funded by' or 'Gifted' alone is not enough; any payment, loan or incentive counts.",
        "email_language": "en-GB",
        "confidence": "medium",
        "notes": "TikTok 0.95 rests on InfluencerFee's 5-10 point gap; Kolect UK/IE medians point the other way, so 1.0 is also defensible.",
        "sources": ["kolect_rates", "kolect_cpm", "influencerfee", "diw_cpm", "milx_cpm", "fed_g5", "vatupdate", "asa_guide", "asa_advice", "lewis_silkin_asa", "assumption"]
      },
      "DE": {
        "name": "Germany",
        "currency": "EUR",
        "fx_per_usd": 0.893,
        "fx_as_of": "2026-10 (monthly avg)",
        "fx_source": "fed_g5",
        "rounding": 10,
        "tax": { "name": "USt (MwSt)", "pct": 19, "note": "Quote 'zzgl. MwSt.'; add the line only if the creator is VAT-registered." },
        "factor_by_tier": { "nano": 0.75, "micro": 0.8, "mid": 0.8, "macro": 0.8, "mega": 0.85 },
        "platform_multipliers": { "instagram": 1.0, "tiktok": 0.9, "youtube": 1.0, "youtube_short": 1.0 },
        "unavailable_platforms": [],
        "disclosure": "Prominent 'Werbung' or 'Anzeige' label at the start; stricter than the US on gifted products, which also need a label.",
        "email_language": "de-DE (formal Sie)",
        "confidence": "low",
        "notes": "Usage buyouts quoted at 25-200% of fee for long, OOH or multi-country terms; keep global add-on % and cap perpetual/OOH at 200%.",
        "sources": ["kolect_rates", "kolect_cpm", "influencerfee", "diw_cpm", "milx_cpm", "kolsquare_de", "fed_g5", "vatupdate", "nyu_jipel", "assumption"]
      },
      "BR": {
        "name": "Brazil",
        "currency": "BRL",
        "fx_per_usd": 5.1298,
        "fx_as_of": "2026-10 (monthly avg)",
        "fx_source": "fed_g5",
        "rounding": 50,
        "tax": {
          "name": "ISS / CBS+IBS",
          "pct": null,
          "note": "Municipal ISS (2-5%, unverified) applies until the CBS/IBS dual-VAT reform completes in 2033. Quote ex-tax ('+ impostos'); no tax line by default."
        },
        "factor_by_tier": { "nano": 0.2, "micro": 0.25, "mid": 0.38, "macro": 0.5, "mega": 0.55 },
        "platform_multipliers": { "instagram": 1.0, "tiktok": 1.0, "youtube": 1.0, "youtube_short": 1.0 },
        "unavailable_platforms": [],
        "disclosure": "CONAR influencer guide (effective 1 Jun 2026): clear ad identification; affiliate or commission links count as advertising; brand and creator share responsibility.",
        "email_language": "pt-BR",
        "confidence": "medium",
        "notes": "Mega capped at India's 0.55 because the only 1M+ source mixes in celebrities. No TikTok/YouTube BRL data; base factor used.",
        "sources": ["veeras", "inteligenciasetorial", "agenciagram", "influencerfee", "diw_cpm", "fed_g5", "kpmg_br", "conar_propmark", "conar_contabeis", "conar_uai", "assumption"]
      },
      "ID": {
        "name": "Indonesia",
        "currency": "IDR",
        "fx_per_usd": 18255,
        "fx_as_of": "2026-11-19",
        "fx_source": "bisnis_idr",
        "rounding": 100000,
        "tax": {
          "name": "PPN (VAT)",
          "pct": 12,
          "note": "12% headline rate (PwC); effective rate on services may be 11% (unverified). Quote ex-PPN; add the line only if the creator is registered."
        },
        "factor_by_tier": { "nano": 0.15, "micro": 0.25, "mid": 0.35, "macro": 0.4, "mega": 0.45 },
        "platform_multipliers": { "instagram": 1.0, "tiktok": 2.0, "youtube": 1.0, "youtube_short": 1.0 },
        "unavailable_platforms": [],
        "disclosure": "Clear sponsored label on every paid post; local rule specifics (ad ethics code EPI) not verified.",
        "email_language": "id-ID",
        "confidence": "medium",
        "notes": "TikTok priced 1.5-2x Instagram locally; 2.0 converts that to BVAL's TikTok unit, which is 0.6x the Reel CPM in the US. Social platforms may not process payments: in-app checkout must run via TikTok Shop/Tokopedia (red flag otherwise). Whitelisting/dark posts are a separately priced right.",
        "sources": ["contentgrip_id", "contentgrip_cost", "influencerfee", "diw_cpm", "bisnis_idr", "pwc_vat", "apf_id", "jakartapost_id", "dfdl_id", "assumption"]
      },
      "MX": {
        "name": "Mexico",
        "currency": "MXN",
        "fx_per_usd": 18.4464,
        "fx_as_of": "2026-10 (monthly avg)",
        "fx_source": "fed_g5",
        "rounding": 100,
        "tax": { "name": "IVA", "pct": 16, "note": "16% is unverified in this research; confirm before showing a tax line. Quote '+ IVA'." },
        "factor_by_tier": { "nano": 0.22, "micro": 0.3, "mid": 0.4, "macro": 0.5, "mega": 0.55 },
        "platform_multipliers": { "instagram": 1.0, "tiktok": 1.0, "youtube": 1.0, "youtube_short": 1.0 },
        "unavailable_platforms": [],
        "disclosure": "Clear sponsored label on every paid post; PROFECO / consumer-law specifics not verified.",
        "email_language": "es-MX",
        "confidence": "low",
        "notes": "No credible tiered MXN rate card exists; Expansion reports no per-deal data until a 2027 industry mapping. Factors rest on the YouTube CPM ratio (above Brazil's) and InfluencerFee.",
        "sources": ["influencerfee", "diw_cpm", "ytmoney_cpm", "expansion_mx", "cronoshare_mx", "fed_g5", "assumption"]
      },
      "CA": {
        "name": "Canada",
        "currency": "CAD",
        "fx_per_usd": 1.4135,
        "fx_as_of": "2026-10 (monthly avg)",
        "fx_source": "fed_g5",
        "rounding": 10,
        "tax": { "name": "GST/HST", "pct": 5, "note": "Federal GST 5% plus provincial PST/HST that varies by province. Quote '+ applicable taxes'." },
        "factor_by_tier": { "nano": 0.85, "micro": 0.9, "mid": 0.9, "macro": 0.95, "mega": 0.95 },
        "platform_multipliers": { "instagram": 1.0, "tiktok": 0.95, "youtube": 1.0, "youtube_short": 1.0 },
        "unavailable_platforms": [],
        "disclosure": "Ad Standards: #ad or #sponsored up front in each post (not #partner or #brand); a one-time bio disclosure is not enough.",
        "email_language": "en-CA (fr-CA for Quebec)",
        "confidence": "low",
        "notes": "Sources conflict: Kolect per-view 1.19x US vs InfluencerFee ~0.70x; 0.90 is the blend.",
        "sources": ["kolect_rates", "kolect_cpm", "influencerfee", "diw_cpm", "milx_cpm", "fed_g5", "vatupdate", "creatordb_reg", "assumption"]
      }
    },
    "groups": {
      "tier1_english": {
        "name": "Other Tier-1 English",
        "members": ["AU", "NZ", "IE", "JE", "GG", "IM"],
        "factor_by_tier": { "nano": 0.8, "micro": 0.85, "mid": 0.85, "macro": 0.9, "mega": 0.9 },
        "fallback_currency": "USD",
        "member_currency": { "AU": "AUD", "NZ": "NZD", "IE": "EUR", "JE": "GBP", "GG": "GBP", "IM": "GBP" },
        "email_language": "en",
        "confidence": "medium",
        "sources": ["kolect_rates", "kolect_cpm", "influencerfee", "diw_cpm", "milx_cpm", "ytmoney_cpm"]
      },
      "western_europe": {
        "name": "Western Europe and Nordics",
        "members": ["FR", "NL", "BE", "LU", "AT", "CH", "LI", "MC", "SE", "NO", "DK", "FI", "IS", "FO", "GL", "AX", "PM"],
        "factor_by_tier": { "nano": 0.65, "micro": 0.7, "mid": 0.7, "macro": 0.72, "mega": 0.75 },
        "fallback_currency": "USD",
        "member_currency": {
          "FR": "EUR",
          "NL": "EUR",
          "BE": "EUR",
          "LU": "EUR",
          "AT": "EUR",
          "MC": "EUR",
          "FI": "EUR",
          "CH": "CHF",
          "LI": "CHF",
          "SE": "SEK",
          "NO": "NOK",
          "DK": "DKK",
          "AX": "EUR",
          "PM": "EUR"
        },
        "email_language": "en",
        "confidence": "low",
        "notes": "France (largest member) derives at 0.62-0.70; lifted slightly for NL/CH/Nordics, whose ad CPMs sit near Germany's. FR labels require specific wording; FR rate cards quote ex-media-rights.",
        "sources": ["kolect_rates", "kolect_cpm", "influencerfee", "diw_cpm", "milx_cpm", "ytmoney_cpm", "matriochka", "dla_piper", "assumption"]
      },
      "southern_europe": {
        "name": "Southern Europe and Israel",
        "members": ["ES", "IT", "PT", "GR", "MT", "CY", "AD", "SM", "VA", "GI", "IL"],
        "factor_by_tier": { "nano": 0.52, "micro": 0.57, "mid": 0.57, "macro": 0.6, "mega": 0.62 },
        "fallback_currency": "USD",
        "member_currency": { "ES": "EUR", "IT": "EUR", "PT": "EUR", "GR": "EUR", "MT": "EUR", "CY": "EUR", "AD": "EUR", "SM": "EUR", "VA": "EUR" },
        "email_language": "en",
        "confidence": "low",
        "notes": "ES ~0.60 and IT ~0.57 from Kolect per-view with a 0.9 haircut. IL placed here by assumption.",
        "sources": ["kolect_rates", "kolect_cpm", "ytmoney_cpm", "dla_piper", "assumption"]
      },
      "eastern_europe": {
        "name": "Central and Eastern Europe",
        "members": ["PL", "CZ", "SK", "HU", "RO", "BG", "HR", "SI", "RS", "BA", "ME", "MK", "AL", "XK", "UA", "MD", "EE", "LV", "LT", "BY", "RU"],
        "factor_by_tier": { "nano": 0.2, "micro": 0.25, "mid": 0.28, "macro": 0.32, "mega": 0.35 },
        "fallback_currency": "USD",
        "member_currency": { "SK": "EUR", "SI": "EUR", "EE": "EUR", "LV": "EUR", "LT": "EUR", "HR": "EUR" },
        "email_language": "en",
        "confidence": "very_low",
        "notes": "YouTube CPM ratio 0.12-0.25 (PL 0.25), nudged up per the emerging-market pattern. RU/BY not covered by any source.",
        "sources": ["ytmoney_cpm", "assumption"]
      },
      "turkiye_central_asia": {
        "name": "Turkiye, Caucasus and Central Asia",
        "members": ["TR", "AZ", "GE", "AM", "KZ", "UZ", "KG", "TJ", "TM", "MN"],
        "factor_by_tier": { "nano": 0.15, "micro": 0.2, "mid": 0.25, "macro": 0.3, "mega": 0.35 },
        "fallback_currency": "USD",
        "member_currency": {},
        "email_language": "en",
        "confidence": "very_low",
        "notes": "Turkiye YouTube CPM ratio 0.07 (DIW) / 0.12 (RevenueLab) scaled by the India pattern; no rate cards.",
        "sources": ["diw_cpm", "ytmoney_cpm", "assumption"]
      },
      "latin_america": {
        "name": "Latin America and Caribbean (ex BR, MX)",
        "members": ["AR", "CO", "CL", "PE", "EC", "UY", "PY", "BO", "VE", "CR", "PA", "GT", "HN", "SV", "NI", "BZ", "DO", "CU", "HT", "JM", "TT", "BS", "BB", "LC", "VC", "GD", "AG", "DM", "KN", "GY", "SR", "PR", "VI", "AW", "CW", "SX", "BQ", "KY", "BM", "TC", "VG", "AI", "MS", "GF", "GP", "MQ", "BL", "MF", "FK"],
        "factor_by_tier": { "nano": 0.18, "micro": 0.22, "mid": 0.32, "macro": 0.42, "mega": 0.45 },
        "fallback_currency": "USD",
        "member_currency": {},
        "email_language": "es",
        "confidence": "low",
        "notes": "Set just below Brazil/Mexico: CO/AR CPMs (0.08-0.11 of US) trail BR/MX (0.12-0.14).",
        "sources": ["ytmoney_cpm", "influencerfee", "assumption"]
      },
      "south_asia": {
        "name": "South Asia (ex IN)",
        "members": ["PK", "BD", "LK", "NP", "BT", "MV", "AF"],
        "factor_by_tier": { "nano": 0.15, "micro": 0.18, "mid": 0.28, "macro": 0.38, "mega": 0.4 },
        "fallback_currency": "USD",
        "member_currency": { "LK": "LKR" },
        "email_language": "en",
        "confidence": "very_low",
        "notes": "PK/BD YouTube CPM 1.00 vs India 1.50; India's factors scaled by ~0.7.",
        "sources": ["ytmoney_cpm", "assumption"]
      },
      "southeast_asia": {
        "name": "Southeast Asia (ex ID)",
        "members": ["PH", "VN", "TH", "MY", "KH", "MM", "LA", "BN", "TL"],
        "factor_by_tier": { "nano": 0.15, "micro": 0.2, "mid": 0.25, "macro": 0.3, "mega": 0.3 },
        "fallback_currency": "USD",
        "member_currency": { "PH": "PHP", "TH": "THB", "MY": "MYR" },
        "email_language": "en",
        "confidence": "low",
        "notes": "Anchored on the Philippines (DMSM nano PHP 1,000-5,000; mega from PHP 150,000) and InfluencerFee's SEA index 10-25.",
        "sources": ["spiralytics_ph", "influencerfee", "ytmoney_cpm", "inquirer_php", "assumption"]
      },
      "east_asia_developed": {
        "name": "Developed East Asia (ex CN)",
        "members": ["JP", "KR", "TW", "HK", "MO", "SG"],
        "factor_by_tier": { "nano": 0.6, "micro": 0.6, "mid": 0.65, "macro": 0.65, "mega": 0.65 },
        "fallback_currency": "USD",
        "member_currency": { "JP": "JPY", "KR": "KRW", "TW": "TWD", "HK": "HKD", "SG": "SGD" },
        "email_language": "en",
        "confidence": "low",
        "notes": "Japan derives at 0.70-0.75 (YouTube ~1.0) and Singapore at ~0.30; KR/TW CPM ratios 0.42-0.44. Japan is under-priced here by ~15%; promote JP to a named country first.",
        "sources": ["tatap", "influencerfee", "ytmoney_cpm", "diw_cpm", "assumption"]
      },
      "gulf": {
        "name": "Gulf (GCC)",
        "members": ["AE", "SA", "QA", "KW", "BH", "OM"],
        "factor_by_tier": { "nano": 0.5, "micro": 0.55, "mid": 0.55, "macro": 0.6, "mega": 0.65 },
        "fallback_currency": "USD",
        "member_currency": {},
        "email_language": "en",
        "confidence": "very_low",
        "notes": "UAE 0.55-0.70 (InfluencerFee only); Saudi ad CPM sources disagree ~3x.",
        "sources": ["influencerfee", "ytmoney_cpm", "diw_cpm", "keepface_ae", "assumption"]
      },
      "mena_other": {
        "name": "Rest of Middle East and North Africa",
        "members": ["EG", "MA", "DZ", "TN", "LY", "SD", "JO", "LB", "IQ", "SY", "YE", "PS", "IR", "EH"],
        "factor_by_tier": { "nano": 0.12, "micro": 0.15, "mid": 0.2, "macro": 0.25, "mega": 0.3 },
        "fallback_currency": "USD",
        "member_currency": {},
        "email_language": "en",
        "confidence": "very_low",
        "sources": ["ytmoney_cpm", "assumption"]
      },
      "sub_saharan_africa": {
        "name": "Sub-Saharan Africa",
        "members": ["NG", "ZA", "KE", "GH", "ET", "TZ", "UG", "RW", "SN", "CI", "CM", "AO", "MZ", "ZM", "ZW", "BW", "NA", "MW", "MG", "MU", "SC", "CD", "CG", "GA", "GQ", "BJ", "TG", "BF", "ML", "NE", "TD", "CF", "SS", "ER", "DJ", "SO", "GM", "GN", "GW", "SL", "LR", "CV", "ST", "KM", "LS", "SZ", "MR", "RE", "YT"],
        "factor_by_tier": { "nano": 0.12, "micro": 0.15, "mid": 0.2, "macro": 0.25, "mega": 0.3 },
        "fallback_currency": "USD",
        "member_currency": { "ZA": "ZAR" },
        "email_language": "en",
        "confidence": "very_low",
        "notes": "YouTube CPM ratio 0.08-0.18 (ZA highest).",
        "sources": ["ytmoney_cpm", "assumption"]
      },
      "rest_of_world": {
        "name": "Catch-all for any unlisted code (Pacific islands etc.)",
        "members": ["FJ", "PG", "SB", "VU", "WS", "TO", "KI", "TV", "NR", "FM", "MH", "PW", "NC", "PF", "GU", "AS", "MP", "CK", "NU", "KP", "UM", "SH", "PN", "TK", "WF", "NF", "CX", "CC", "IO", "AQ", "BV", "HM", "TF", "GS", "SJ"],
        "factor_by_tier": { "nano": 0.15, "micro": 0.2, "mid": 0.25, "macro": 0.3, "mega": 0.35 },
        "fallback_currency": "USD",
        "member_currency": {},
        "email_language": "en",
        "confidence": "very_low",
        "sources": ["assumption"],
        "notes": "Engine maps ANY code not found in countries, groups or unsupported here."
      }
    },
    "unsupported": ["CN"],
    "unsupported_reason": { "CN": "Instagram, YouTube and international TikTok are unavailable; creators use Douyin, RED and Bilibili." },
    "fx": {
      "note": "Group member currencies for optional local display; named countries carry their own fx_per_usd.",
      "as_of": "2026-10 (monthly avg) unless stated",
      "source": "fed_g5",
      "per_usd": {
        "EUR": 0.893,
        "GBP": 0.7523,
        "AUD": 1.431,
        "NZD": 1.774,
        "CHF": 0.8289,
        "SEK": 9.96,
        "NOK": 9.45,
        "DKK": 6.68,
        "JPY": 157.9748,
        "KRW": 1337.36,
        "TWD": 32.27,
        "HKD": 7.85,
        "SGD": 1.2801,
        "THB": 33.65,
        "MYR": 4.08,
        "LKR": 331.4,
        "ZAR": 16.57,
        "PHP": 62.87
      },
      "exceptions": {
        "PHP": { "as_of": "2026-10-14", "source": "inquirer_php" }
      }
    },
    "sources": {
      "assumption": "BVAL design choice or interpolation; not a published figure",
      "madison_wall": "https://www.netinfluencer.com/advertiser-spending-on-creators-to-reach-116b-usd-in-2026-report-shows/",
      "datareportal_ig": "https://datareportal.com/essential-instagram-stats",
      "datareportal_tt": "https://datareportal.com/essential-tiktok-stats",
      "datareportal_yt": "https://datareportal.com/essential-youtube-stats",
      "leaddyno": "https://www.leaddyno.com/blog/influencer-pricing",
      "later2026": "https://later.com/blog/influencer-pricing-benchmarks-the-complete-2026-guide/",
      "grynow": "https://www.grynow.in/blog/influencer-marketing-cost-in-india.html",
      "upgrowth": "https://upgrowth.in/influencer-marketing-pricing-india-2026/",
      "tryspansa": "https://dev.to/tryspansa/influencer-rate-card-what-brands-should-pay-43oj",
      "influencerfee": "https://influencerfee.com/blog/influencer-pricing-by-country/",
      "kolect_rates": "https://www.kolect.ai/guides/influencer-rates",
      "kolect_cpm": "https://www.kolect.ai/reports/influencer-cpm-benchmarks-2026",
      "diw_cpm": "https://www.digitalinformationworld.com/2025/08/youtube-cpm-rates-in-2025-how-location.html",
      "milx_cpm": "https://milx.app/trends/which-countries-have-the-best-youtube-cpm-rates-in-2025",
      "ytmoney_cpm": "https://ytmoneycalculator.com/blog/youtube-cpm-rates-by-country/",
      "kolsquare_de": "https://www.kolsquare.com/de/blog/wie-viel-kostet-influencer-marketing-im-jahr-2025",
      "matriochka": "https://www.cbnews.fr/node/102945",
      "veeras": "https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital",
      "inteligenciasetorial": "https://inteligenciasetorial.com.br/marketing/quanto-cobrar-por-publipost-no-tiktok/",
      "agenciagram": "https://agenciagram.com.br/blog/como-ser-micro-influenciador-instagram-2026",
      "contentgrip_id": "https://contentgrip.com/influencer-marketing-indonesia/",
      "contentgrip_cost": "https://contentgrip.com/influencer-marketing-cost/",
      "expansion_mx": "https://expansion.mx/mercadotecnia/2026/10/13/cuanto-dinero-llega-influencers-intermediacion-calculo",
      "cronoshare_mx": "https://www.cronoshare.com.mx/cuanto-cuesta/contratar-influencer",
      "tatap": "https://tatap.jp/knowledge/influencer-marketing-costs/",
      "spiralytics_ph": "https://www.spiralytics.com/blog/influencer-marketing-philippines",
      "keepface_ae": "https://keepface.com/site/?p=8751",
      "fed_g5": "https://www.federalreserve.gov/releases/g5/20261102/",
      "hdfc_fx_1": "https://hdfcsky.com/news/rupee-rises-24-paise-to-93-27-against-us-dollar-in-early-trade-november-18-2026",
      "hdfc_fx_2": "https://hdfcsky.com/news/rupee-falls-8-paise-to-close-at-94-20-against-us-dollar",
      "bisnis_idr": "https://market.bisnis.com/read/20261119/93/2022767/rupiah-ditutup-melemah-ke-rp18255-per-dolar-as-hari-ini-1911",
      "inquirer_php": "https://business.inquirer.net/617575/peso-breaches-63-61-level",
      "taxmann": "https://www.taxmann.com/post/blog/opinion-impact-of-gst-on-social-media-influencers/",
      "taxaj": "https://www.taxaj.com/learn/gst-and-income-tax-for-influencers-and-content-creators-in-india-2026/",
      "vatupdate": "https://www.vatupdate.com/2026/07/25/global-vat-rates-by-country-2026-standard-and-reduced-rates/",
      "pwc_vat": "https://taxsummaries.pwc.com/quick-charts/value-added-tax-vat-rates",
      "kpmg_br": "https://kpmg.com/kpmg-us/content/dam/kpmg/taxnewsflash/pdf/2026/digitalized-economy-taxation-developments-summary.pdf",
      "nyu_jipel": "https://jipel.law.nyu.edu/disclosure-requirements-for-influencer-marketing-in-the-u-s-and-germany/",
      "asa_guide": "https://www.asa.org.uk/resource/influencers-guide.html",
      "asa_advice": "https://www.asa.org.uk/news/ad-vice-making-clear-that-an-ad-is-an-ad.html",
      "lewis_silkin_asa": "https://www.lewissilkin.com/insights/2026/10/23/new-influencer-guidance-from-the-asa-cap-and-cma-what-has-changed-and-what-to-d-102o6ar",
      "asci_pdf": "https://www.ascionline.in/social/wp-content/uploads/2025/04/ASCI-Influencer-Guidelines.pdf",
      "asci_dos": "https://www.ascionline.in/social/dos-dont/",
      "conar_propmark": "https://propmark.com.br/artigos/o-novo-guia-do-conar-para-influenciadores-e-os-riscos-da-falta-de-transparencia/",
      "conar_contabeis": "https://www.contabeis.com.br/artigos/77061/conar-novas-regras-para-influenciadores-e-ia-a-partir-de-1o-de-junho/",
      "conar_uai": "https://www.uai.com.br/networking-e-negocios/2026/09/23/ganha-comissao-com-link-de-afiliado-para-o-conar-isso-ja-e-publicidade/",
      "creatordb_reg": "https://creatordb.app/blog/regulation-english/",
      "dla_piper": "https://www.dlapiper.com/news/2025/09/dla-piper-unpacks-influencer-marketing-rules-with-updated-and-expanded-global-guide",
      "macrumors_tt": "https://www.macrumors.com/2026/01/23/tiktok-avoids-us-ban-deal-officially-closes/",
      "businesstoday_tt": "https://www.businesstoday.in/india/story/no-comeback-for-tiktok-indian-govt-refutes-reports-of-ban-being-lifted-on-chinese-apps-490769-2025-08-23",
      "techcrunch_tt": "https://techcrunch.com/2025/08/22/tiktok-denies-india-comeback-after-reports-of-website-going-live",
      "patrika_tt": "https://www.patrika.com/en/national-news/tiktok-ban-in-india-not-lifted-says-modi-government-19886142",
      "apf_id": "https://www.asiapacific.ca/publication/indonesias-new-e-commerce-regulations-take-bite-out-tiktoks",
      "jakartapost_id": "https://www.thejakartapost.com/business/2023/09/27/indonesia-bans-goods-transactions-on-social-media-platforms",
      "dfdl_id": "https://www.dfdl.com/insights/legal-and-tax-updates/indonesia-ecommerce-regulation-permendag-19-2026/"
    }
  }
}
```

## The counter-offer email adapts in three places

The email prompt takes three extra fields: `email_language`, `disclosure` and `tax`. **Language** defaults to the market's `email_language`: pt-BR, es-MX, id-ID, de-DE with formal *Sie*, and English variants elsewhere, with fr-CA offered for Québec. A user `email_language` input overrides it, and English stays a one-click alternative everywhere, since brand deals in India and most groups run in English. The language choice for Brazil, Mexico, Indonesia and Germany is an inference and has not been tested against creators. Numbers keep local formatting and the currency the user chose. The LLM must still use only figures from the input JSON.

**Disclosure** adds one sentence to the terms block: "Content will carry the [label] disclosure required by [regulator]." Examples are #ad under ASA/CMA in the UK ([ASA](https://www.asa.org.uk/resource/influencers-guide.html)), an ASCI-listed label such as "Ad" or "Collaboration" in India ([ASCI](https://www.ascionline.in/social/wp-content/uploads/2025/04/ASCI-Influencer-Guidelines.pdf)), "Werbung" in Germany ([NYU JIPEL](https://jipel.law.nyu.edu/disclosure-requirements-for-influencer-marketing-in-the-u-s-and-germany/)), CONAR identification in Brazil, where affiliate links count as advertising since 1 June 2026 ([Propmark](https://propmark.com.br/artigos/o-novo-guia-do-conar-para-influenciadores-e-os-riscos-da-falta-de-transparencia/)), and #ad or #sponsored, never #partner, in Canada ([CreatorDB](https://creatordb.app/blog/regulation-english/)). Four new red flags feed the pushback section. `NO_AD_LABEL` fires when the brief asks for no label, or only "gifted"/"#partner". `NONSTANDARD_LABEL_IN` fires for a label outside the ASCI list. `AFFILIATE_UNLABELED_BR` fires for an affiliate deal in Brazil with no label. `ID_OFFPLATFORM_CHECKOUT` fires when an Indonesian brief needs checkout outside TikTok Shop or Tokopedia.

**Ex-tax note**: the quote line carries the local suffix ("+ VAT", "zzgl. MwSt.", "+ 18% GST", "+ IVA", "+ applicable taxes"). The tax amount appears only when the creator is registered. For US markets no tax text is added.

## Limitations to show in the output

No public source publishes prices by country, tier and platform from transaction data, so every factor here is **derived**. Kolect gives country medians without tiers. InfluencerFee is algorithmic and does not disclose its method. Ad-CPM ratios understate creator prices in emerging markets by 2–7×, and in Japan they get even the direction wrong. The tier shapes for developed markets are judgment calls. Mexico, Canada, the Gulf, Türkiye, Eastern Europe, South Asia, MENA and Africa all rest on one source or on CPM scaling alone, and Indonesia's TikTok ×2.0 is a tempered conversion rather than a measured value. Local rate cards lag FX movements, and BRL, IDR and PHP weakened in 2026, so USD factors there may drift about 5–10% low unless they are recalibrated ([Inquirer](https://business.inquirer.net/617575/peso-breaches-63-61-level)). Several practicalities were not verified: Mexico's IVA, Indonesia's 11% effective PPN, Brazil's ISS rates, US sales tax by state, and the disclosure rules in Mexico and Indonesia. Their JSON entries say so, and the email should state them as general guidance only. Return the market's `confidence`, show `matched: "group"` prominently, and keep the existing disclaimer. Group fallbacks are intended to give a sensible starting point for negotiation, not a precise local rate.

## Conclusion

Supporting more countries turns out to be mostly a data-maintenance job rather than a change to the pricing model. The same view-based engine, with one multiplier applied after the clamp, holds up in every market, because add-on percentages and negotiation logic do not visibly change between countries. What does vary by country is presentation and compliance: currency, tax label, disclosure wording and which platforms are allowed. The largest pricing risk is not the factor values. It is semantic errors like the Indonesian TikTok case, where a premium measured against one baseline is applied to another. Calibration should therefore start where the user base will grow: price 5–10 known Indonesian, Brazilian and Mexican deals per platform, then promote Japan to a named country. After that, groups can be replaced by named countries one at a time as real deal data comes in.
