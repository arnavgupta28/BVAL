# Steps: BVAL, brand-deal rate calculator (Apify Actor)

**Status key:** ✅ Done · 🔄 Working · ⏳ Upcoming · 🟡 In review (needs your confirmation or action)

Actor: **BVAL** (title) / **`bval`** (ID). Team name on the submission form must be "BVAL". Logo: [logo/bval-logo-512.png](logo/bval-logo-512.png). Code: [bval/](bval/). Research: [bval_research.md](bval_research.md), [reports/BVAL country market factors.md](reports/BVAL%20country%20market%20factors.md).

**What it does:** creator handle + brand's deal terms → fair rate, itemised add-ons (usage, Partnership/Spark Ads, exclusivity, rush, …), walk-away/floor/fair/ask range, verdict on the offer, red flags, and a ready-to-send counter-offer email. Instagram, TikTok, YouTube (Shorts + long-form). Any country.

**The one rule:** public on Apify Store and running live in the 2-minute demo (14:30). **Milestone:** first successful cloud run + publish ASAP.

---

## Step 0: Lock the basics
- ✅ Name **BVAL** / `bval`; logo made ([svg](logo/bval-logo.svg), [512px](logo/bval-logo-512.png), [128px](logo/bval-logo-128.png)).
- ✅ Buyer persona: *Priya, 85k-follower fitness creator; Acme Protein offers $800 for a Reel + 90d usage + 30d Partnership Ads + 180d exclusivity.* Secondary: talent managers/agencies (bulk, API/MCP).
- ✅ Platforms: Instagram, TikTok, YouTube (Shorts + long-form), each priced on its own value proposition.
- ✅ Markets: any country via `market` (8 named: US, IN, GB, DE, BR, ID, MX, CA + 13 regional groups); computed in USD, optional local currency.
- ✅ Language: Python (`python-empty` template, package `my_actor`).

## Step 1: Account and tooling
- ✅ Apify CLI 1.13.0 installed; logged in as `agupta1`.
- ✅ Apify agent skills installed (`apify-actor-development`, `apify-ultimate-scraper`).
- ✅ Coupon **`APIFYBLR`** applied ($50 credit).
- 🟡 Billing/payment details filled in and **Store Publishing Terms** accepted (needed for pricing + publishing). *Please confirm.*
- ✅ Public GitHub repo: [arnavgupta28/BVAL](https://github.com/arnavgupta28/BVAL) (initial commit pushed; `assets/`, `storage/`, `.venv`, `.env` ignored).
- ✅ Today's work committed and pushed (`077e7d0`).
- ⏳ Run instructions in the repo README (with Step 10).

## Step 2: Research (pricing must hold up against market data)
- ✅ Deep research on rates, add-ons, negotiation, competitors, feeders → [bval_research.md](bval_research.md) with cited `rates.json` (67 source entries).
- ✅ Country research → 8 named markets + 13 regional groups, FX, tax, platform bans, disclosure rules → [country report](reports/BVAL%20country%20market%20factors.md).

## Step 3: Feeder Actors verified with real runs ($0.33 total)
- ✅ Instagram: `apify/instagram-profile-scraper` (10s, $0.003) + `apify/instagram-reel-scraper` (39s, $0.08). `videoPlayCount` populated 30/30.
- ✅ TikTok: `clockworks/tiktok-profile-scraper` (14s, $0.09). All fields populated.
- ✅ YouTube: `streamers/youtube-scraper` (57s, $0.16). Absolute dates + likes present.
- ✅ Fixtures saved in [bval/tests/fixtures/](bval/tests/fixtures/).

## Step 4: Scaffold
- ✅ `apify create bval -t python-empty`; `meta.generatedBy` set; title/description in [actor.json](bval/.actor/actor.json).

## Step 5: Core logic
- ✅ Pricing engine [pricing.py](bval/my_actor/pricing.py) + [rates.json](bval/my_actor/config/rates.json): views × CPM × ratio × niche → ER adjustment → tier clamp → market factor → package discount → add-ons → walk-away/floor/fair/ask → verdict → red flags → reduced-scope option → confidence.
- ✅ Markets: `resolve_market` (alias → country → regional group → global), TikTok blocked in India, China refused, offers in 11 currencies.
- ✅ Feeders [feeders.py](bval/my_actor/feeders.py): parallel IG calls, cost/time caps per call, age windows with fallback, 0/-1 treated as missing.
- ✅ Counter-offer email [counter_email.py](bval/my_actor/counter_email.py): LLM via Apify OpenRouter proxy, brand-facing pushback lines, deterministic template fallback.
- ✅ LLM email works on the platform (`anthropic/claude-sonnet-4.5` via Apify OpenRouter). Only local runs get 403 and fall back to the template.
- ✅ Entry point [main.py](bval/my_actor/main.py): input → scrape or manual metrics → price → email → PPE charges → dataset row + `QUOTE.md`.
- ✅ Tests: **40 passing** (3 research worked examples, real fixtures, markets, edge cases): `cd bval && .venv/bin/python -m unittest discover -s tests`.

## Step 6: Schemas (Craft)
- ✅ [input_schema.json](bval/.actor/input_schema.json): sections for offer, usage/ads/exclusivity, production, contract, market/email, advanced; prefilled demo values.
- ✅ [dataset_schema.json](bval/.actor/dataset_schema.json): 32 fields; views "Deal verdict" and "Line items".
- ✅ [output_schema.json](bval/.actor/output_schema.json) + [key_value_store_schema.json](bval/.actor/key_value_store_schema.json) (`QUOTE.md`).
- ✅ `apify validate-schema` passes.

## Step 7: Run locally, push, first cloud run
- ✅ Local `apify run` (manual metrics): fair $2,790, verdict DECLINE_OR_REDUCE_SCOPE, `QUOTE.md` written.
- ✅ `apify push`: build **0.1.3** live ([Console](https://console.apify.com/actors/pvlXeWRnGfAg9NI0j)). Fixed on the way: child runs need `run_name`; dropped deprecated `max_items`.
- ✅ First cloud run **SUCCEEDED in 56s** on @humansofny: real scrape, verdict, LLM email ([run](https://console.apify.com/actors/runs/9ebRSTXyVTfJuwTYv)).
- 🟡 Check the Output tab in Console: "Deal verdict" view and `QUOTE.md` render. *Take a look at the run link.*

## Step 8: Publish on the Store (Console → My Actors → bval → Publishing)
- ⏳ Display info: title, description, upload [logo/bval-logo-512.png](logo/bval-logo-512.png).
- ⏳ Categories: AI, Social media, Marketing/Business.
- ⏳ Sample output from the successful run; permissions **limited**.
- 🟡 Billing details + Store Publishing Terms (you, in Console), then monetization (Step 9).
- ⏳ Publish on Store; copy the **direct Store URL** for judges.

## Step 9: Pricing model, pay-per-event
- ✅ Charges wired in code, only after success: `deal-evaluated`, `manual-deal-evaluated`, `counter-email-drafted`.
- ✅ Prices confirmed: `deal-evaluated` **$0.79**, `counter-email-drafted` **$0.20**, `manual-deal-evaluated` **$0.25** (full deal $0.99).
- 🟡 Enter them in Console → bval → Publication → Monetization → Pay per event (after billing details). Until then the Actor logs "ignored charge" and still runs.
- ⏳ Turn off the synthetic per-dataset-item event; do not enable "PPE + usage".

## Step 10: README that sells
- 🔄 Writing next: hero line, buyer, problem, output screenshot, how it works (scrapers → engine → email), platform value props, markets, input table, sample output, pricing, integrations (API/MCP/agents), FAQ/limits, sources, run locally.

## Step 11: Polish
- ✅ `QUOTE.md` Markdown report.
- ✅ Error handling: bad handle, private account, unsupported platform/market → error item + failed run, no charge.
- ✅ Local currency output (`outputCurrency: LOCAL`) for all named markets.
- ✅ All three platforms in v1.
- ⏳ Batch mode (array of handles for agencies). Skip if short on time.
- ⏳ Optional: Japan as a named market (report says its group under-prices it ~15%); one config entry.

## Step 12: Final verification
- ⏳ `apify push` final build; 3 runs from the public Store page (IG, TikTok, YouTube), each under ~60s.
- ⏳ Check Output tab, `QUOTE.md`, README and pricing on the Store page.
- ⏳ Freeze code; push to GitHub.

## Step 13: Demo prep and submit
- ⏳ Pre-run a backup run with the exact demo input; keep the tab open.
- ⏳ Rehearse the 2-minute script twice:
  - **0:00–0:15 buyer:** "Priya got $800 for a Reel + 90 days usage + 30 days of ads through her handle + 6 months exclusivity. Fair?"
  - **0:15–0:25 live run** from the public Store page.
  - **0:25–0:55 while it runs:** "Apify's own Instagram scrapers get her real median Reel plays. The price comes from a cited, transparent engine. The LLM only writes the email."
  - **0:55–1:35 output:** "Fair is $2,790; her $800 is below her walk-away. Exclusivity alone is worth $1,360. Here's the counter: full scope at $3,490, or a lighter version at $1,070, ready to send."
  - **1:35–1:50 money + reach:** "$0.99 a deal, pay-per-event. Any country: the same deal is fair at $698 for an Indian audience. Agencies call it via API or MCP."
  - **1:50–2:00 close:** "BVAL: know your worth before you reply."
- ⏳ Submit the Google Form (team name = BVAL, Store URL, GitHub URL).
- ⏳ Optional: post on LinkedIn/X tagging @apify.

---

### Reference docs
[CLI reference](https://docs.apify.com/cli/docs/reference.md) · [Input schema](https://docs.apify.com/actors/development/actor-definition/input-schema/specification/v1.md) · [Output schema](https://docs.apify.com/actors/development/actor-definition/output-schema.md) · [Dataset schema](https://docs.apify.com/storage/dataset-schema.md) · [Publish](https://docs.apify.com/actors/publishing/publish.md) · [Pay-per-event](https://docs.apify.com/actors/monetize/pay-per-event.md)
