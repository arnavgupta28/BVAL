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
- ✅ Hackathon coupon applied ($50 credit).
- ✅ Billing details and Store Publishing Terms done (monetization and publishing went through, 22 Nov 2026).
- ✅ Public GitHub repo: [arnavgupta28/BVAL](https://github.com/arnavgupta28/BVAL) (initial commit pushed; `assets/`, `storage/`, `.venv`, `.env` ignored).
- ✅ Today's work committed and pushed (`077e7d0`).
- ✅ Run instructions in the repo README.

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
- ✅ Two outputs from one run (22 Nov 2026): visual deal report `QUOTE.html` for people (first in the Output tab, works on a phone, light and dark), and agent fields `nextAction`, `summary` and `reportUrl` at the top of the JSON row. Code in [report.py](bval/my_actor/report.py); schemas and README updated; local run checked.
- ✅ Counter-offer email moved up in `QUOTE.html` (under the verdict) and given its own "Counter-offer email" view in the Output tab.
- ✅ New input `sendReportTo`: emails the verdict, prices, counter-offer email and report link through `apify/send-mail`. Apify only delivers to the running account's own address; other addresses log a clear warning and the run still succeeds. Address is never stored. Real send tested locally (22 Nov 2026) with `BVAL_SEND_EMAIL_LOCALLY=1`; 50 tests passing.
- ✅ `QUOTE.html`, the email view and the agent fields deployed (build **0.1.7**). Scraped cloud run `h2w11aGmUsRUFpXK4` succeeded in 65s; `reportUrl` opens logged out (HTTP 200, signed link).
- ✅ `sendReportTo` delivery verified on the platform in build 0.1.8 (report + counter-offer emails reached your Gmail).
- ✅ (Superseded by 0.1.9 below) Email model briefly reverted to Sonnet 4.5 in 0.1.6/0.1.7 while the 5.5 parse failure was investigated.
- ✅ Email quote adds up: itemised lines are priced at the ask and sum exactly to the quoted total ($1,240 + $200 + $350 + $1,700 = $3,490). [quote_lines](bval/my_actor/counter_email.py#L119); 3 tests in [test_email_quote.py](bval/tests/test_email_quote.py).
- ✅ No-offer mode (22 Nov 2026): tick `offer.noOffer` and BVAL prices the creator's own package (what they fill in) plus a rate card from their numbers: Starter / Standard / Premium packages, price per post for every format, and what each extra adds. Summary lists the packages for agents. Code in [rate_card.py](bval/my_actor/rate_card.py). Form prefill fixed: offer amount 8000 → **800** to match the demo story.
- ✅ "Your numbers, and what they prove" (22 Nov 2026): every stat BVAL pulled (audience, median views, reach, engagement, niche, market, sponsored posts, view consistency) with its benchmark and the effect on the price, ending at the per-post result. In the report, Markdown and the `evidence` field. Code in [evidence.py](bval/my_actor/evidence.py).
- ✅ Designed counter-offer email (22 Nov 2026): the reply to the brand laid out in the report style (quote card, notes list, no BVAL branding), saved as `COUNTER_EMAIL.html`, linked from the report, and sent as a second "Ready to forward" email when `sendReportTo` is set. Sent to your Gmail from local runs of the demo deal and the no-offer case. 75 tests passing.
- ✅ Live in build **0.1.8** (22 Nov 2026). Cloud runs on priya.fit: $800 deal ([nsYxb1wj7HqO0ytbR](https://console.apify.com/actors/runs/nsYxb1wj7HqO0ytbR)) and no offer ([9TQqpTGC2Rjg19SlD](https://console.apify.com/actors/runs/9TQqpTGC2Rjg19SlD)) both succeeded; Sonnet 4.5 wrote both emails; report and designed-email links open logged out; designed email has no BVAL branding; report + counter-offer emails sent to your Gmail.
- ✅ Sonnet 5.5 now writes the emails (build **0.1.9**, run [6fUJ3ufldGrwEWtCu](https://console.apify.com/actors/runs/6fUJ3ufldGrwEWtCu)). Cause of the earlier failure: a strict JSON parse rejected line breaks inside the body; `_parse` now accepts them. Fallbacks: Sonnet 4.5, then gpt-4o-mini.
- 🟡 Local only, ships with the next push: strip Markdown `**bold**` that Sonnet 5.5 adds to the email text.
- ✅ Entry point [main.py](bval/my_actor/main.py): input (grouped or flat) → scrape or manual metrics → price → email → PPE charges → `QUOTE.html` + `QUOTE.md` → optional report email → dataset row.
- ✅ Tests: **75 passing** (research worked examples, real fixtures, markets, inputs, reports, email digest, HTML escaping): `cd bval && .venv/bin/python -m unittest discover -s tests`.

## Step 5b: Mentor feedback ([assets/inputs_from_mentors.md](assets/inputs_from_mentors.md))
| # | Mentor ask | Status | Where |
|---|---|---|---|
| 1 | Mandatory vs optional fields | ✅ | Only `platform` + `handle` required; sections labelled "(required)", "(recommended)", "(optional)" |
| 2 | Seamless, simple journey | ✅ | 7 numbered sections in the order a creator thinks: who → audience → offer → rights → extras → results; demo deal prefilled |
| 3 | Core-value fields vs extra configurability | ✅ | Sections 1–4 carry the value; 5, 6 and Advanced are optional fine-tuning |
| 4 | Usable by people (website/workflow) and agents; show in demo | ✅ / 🟡 | Store form + API/workflows; Claude + Apify MCP agent path in [demo_harness_plan.md](demo_harness_plan.md). Dry-run pending |
| 5 | Self-explanatory inputs | ✅ | Plain-language titles ("You can't work with competitors for (days)"), every field has a description (tested) |
| 6 | Group related fields, nested/hierarchical | ✅ | `offer`, `rights`, `extras`, `contract`, `manualMetrics` objects; `deliverables` list of {type, qty} |
| 7 | Visually rich output for people, rich context for agents | ✅ | `QUOTE.html` report + `nextAction` / `summary` / `reportUrl` agent fields, plus the optional report email |
- ✅ Deployed (grouped input since 0.1.7; live build **0.1.9**), verified in cloud runs.
- 🟡 Look at the new form in Console (Input tab) and say if anything reads oddly.
- 🟡 Git commit + push of everything since `3e5cbe0` (20+ files: inputs, report, rate card, evidence, email fixes, tests, config guide). Decide first where README images live (`assets/` is git-ignored because it holds the coupon notes; suggested: `.gitignore` exception for `assets/readme/` only). *Needs your OK.*

## Step 6: Schemas (Craft)
- ✅ [input_schema.json](bval/.actor/input_schema.json) restructured per mentor feedback: **2 required fields** (platform, handle), 15 top-level fields in 7 numbered sections, nested `offer` / `rights` / `extras` / `contract` / `manualMetrics` objects and a `deliverables` list of {type, qty} rendered as form fields (`schemaBased`), plain-language titles, `market` with country suggestions plus free entry. Validated.
- ✅ [inputs.py](bval/my_actor/inputs.py): `normalize_input()` flattens the groups; old flat inputs still work. 10 tests in [test_inputs.py](bval/tests/test_inputs.py) (grouped = flat, every field has a title and description, only 2 required). Suite now **75 passing**.
- ✅ [dataset_schema.json](bval/.actor/dataset_schema.json): every pushed field, including `nextAction`, `summary`, `reportUrl`, `offerValue`, `reportEmailed`; views "Deal verdict", "Counter-offer email" and "Line items".
- ✅ [output_schema.json](bval/.actor/output_schema.json) (deal report first, then the email, verdict table, Markdown and JSON) + [key_value_store_schema.json](bval/.actor/key_value_store_schema.json) (`QUOTE.html`, `QUOTE.md`).
- ✅ `apify validate-schema` passes.

## Step 7: Run locally, push, first cloud run
- ✅ Local `apify run` (manual metrics): fair $2,790, verdict DECLINE_OR_REDUCE_SCOPE, `QUOTE.md` written.
- ✅ `apify push`: build **0.1.9** live ([Console](https://console.apify.com/actors/pvlXeWRnGfAg9NI0j)). Fixed on the way: child runs need `run_name`; dropped deprecated `max_items`.
- ✅ First cloud run **SUCCEEDED in 56s** on @humansofny: real scrape, verdict, LLM email ([run](https://console.apify.com/actors/runs/9ebRSTXyVTfJuwTYv)).
- 🟡 Check the Output tab in Console: "Deal verdict" view and `QUOTE.md` render. *Take a look at the run link.*

## Step 8: Publish on the Store (Console → My Actors → bval → Publishing)
- ✅ Console config guide with reasoning: [apify_console_config.md](apify_console_config.md).
- ✅ Public profile set up (22 Nov 2026).
- ✅ BVAL logo uploaded as the Actor icon.
- ✅ Display info: title and description set from `actor.json`.
- ✅ Categories: AI, Social media, Marketing.
- ✅ Permissions **limited**; successful runs on 0.1.8 and 0.1.9.
- ✅ Billing details, Store Publishing Terms and monetization done.
- ✅ **Published on Apify Store** (22 Nov 2026): https://apify.com/agupta1/bval (HTTP 200 logged out; build 0.1.9).
- ✅ Display information (22 Nov 2026): SEO title "Brand Deal & Influencer Rate Calculator for Creators | BVAL", SEO description set; categories AI, Social media, Marketing (set through the API).

## Step 9: Pricing model, pay-per-event
- ✅ Charges wired in code, only after success: `deal-evaluated`, `manual-deal-evaluated`, `counter-email-drafted`.
- ✅ Prices confirmed: `deal-evaluated` **$0.79**, `counter-email-drafted` **$0.20**, `manual-deal-evaluated` **$0.25** (full deal $0.99).
- ✅ Pay-per-event live since 08:34 UTC 22 Nov 2026, verified through the API: `deal-evaluated` $0.79 (primary), `counter-email-drafted` $0.20, `manual-deal-evaluated` $0.25 (infrequent), `apify-actor-start` $0.00005; Apify margin 20%. Cost and profit: [BVAL pricing and unit economics](https://claude.ai/artifact/RmxTXatvE864LpsdsTt6G5).
- ✅ Monetization form: `apify-default-dataset-item` removed, "PPE + usage" off, minimum max cost per run $1.00.
- ⏳ Code follow-up: check the remaining spending cap before scraping (guide, open questions).

## Step 10: README that sells
- ✅ Store README [bval/README.md](bval/README.md): hero + Priya example, what it does, who it's for, why, data table, how-to, pricing, formula with sources, input/output examples, MCP/API, FAQ + data disclaimer, run locally. Deployed in build 0.1.4.
- ✅ Repo README [README.md](README.md) with run instructions; pushed (`3e5cbe0`).
- ⏳ Optional: add a screenshot of the Output tab to the README after Console check.

## Step 11: Polish
- ✅ `QUOTE.md` Markdown report and `QUOTE.html` visual report.
- ✅ Report and notification email restyled to match `assets/design` (bright cards, display font, drawn avatar per handle, starbursts and sparkles); 50 tests pass.
- ✅ New look checked before push (22 Nov 2026): 60 tests, local run, page renders, injection test (script/onerror in handle, name, email and red flags) leaves no raw tags in the page or the email.
- ✅ New look live in build 0.1.7.
- ✅ Glass UI and phone layout: report shows as a phone (status bar, glass dock that jumps to Verdict / Reply / Price / Details) on desktop and fills the screen on a phone; glass cards and chips over colour blobs; email is phone-width with glass panels. Tests pass.
- ✅ README graphics in the same style (`assets/readme/`: banner, how it works, who it's for, verdicts, pricing, three-phone output), built by `assets/readme/build_readme_images.py` and placed in both READMEs.
- ✅ Glass/phone report live since build 0.1.8.
- 🟡 README images show on the Store only after they're pushed to GitHub `main` (the Store README loads them from raw.githubusercontent.com). Until then the Store page shows broken images.
- ✅ Error handling: bad handle, private account, unsupported platform/market → error item + failed run, no charge.
- ✅ Local currency output (`outputCurrency: LOCAL`) for all named markets.
- ✅ All three platforms in v1.
- ⏳ Batch mode (array of handles for agencies). Skip if short on time.
- ⏳ Optional: Japan as a named market (report says its group under-prices it ~15%); one config entry.

## Step 12: Final verification
- ⏳ `apify push` final build; 3 runs from the public Store page (IG, TikTok, YouTube), each under ~60s.
- ⏳ Check Output tab (deal report, email view, `QUOTE.md`), README and pricing on the Store page.
- ✅ Cloud run with `sendReportTo` = your Gmail (build 0.1.8): report email and designed counter-offer email both sent.
- ⏳ Freeze code; push to GitHub.

## Step 13: Demo prep and submit
- ⏳ Pre-run a backup run with the exact demo input; keep the tab open.
- ✅ Demo harness decided (revised 22 Nov 2026): our phone-styled pages in [demo/](demo/) for both paths: a "Check a deal" page that runs the live Actor on Apify, and a creator-agent chat page where Claude calls BVAL as a tool. Store page shown as proof it's live; claude.ai + Apify MCP as the agent backup. Plan and script: [demo_harness_plan.md](demo_harness_plan.md).
- ✅ Demo pages + local server ([demo/server.py](demo/server.py), `demo/static/`), built by session apify-4e [fef7ec]. `demo/.venv` created; smoke test: all pages load, missing tokens give clear errors.
- ✅ Agent page runs on a local LLM in LM Studio by default (`qwen/qwen3.5-9b`, 16k context, `http://127.0.0.1:1234/v1`, token from `LM_API_TOKEN`); `AGENT_BACKEND=claude` switches to Claude. Agent tool supports `noOffer`. Every tool call is a live run of the Apify Actor.
- 🟡 Start the demo yourself (tokens only in your terminal): `APIFY_TOKEN=… LM_API_TOKEN=… demo/.venv/bin/python demo/server.py`, then dry-run the agent prompt 3 times.
- ⏳ Dry-run the agent page with the DM prompt (check it fills `offer.amount`, the `rights` days and `niche: fitness`). Backup: add the Apify MCP connector in claude.ai.
- ⏳ Pre-run a no-offer report for the 1:42 beat of the script.
- ⏳ Rehearse the 2-minute script twice: use the version in [demo_harness_plan.md](demo_harness_plan.md) (both paths: Store page and Claude agent). Update the prices in it after the backup run if you demo a scraped handle.
- ⏳ Submit the Google Form (team name = BVAL, Store URL, GitHub URL).
- ⏳ Optional: post on LinkedIn/X tagging @apify.

---

### Reference docs
[CLI reference](https://docs.apify.com/cli/docs/reference.md) · [Input schema](https://docs.apify.com/actors/development/actor-definition/input-schema/specification/v1.md) · [Output schema](https://docs.apify.com/actors/development/actor-definition/output-schema.md) · [Dataset schema](https://docs.apify.com/storage/dataset-schema.md) · [Publish](https://docs.apify.com/actors/publishing/publish.md) · [Pay-per-event](https://docs.apify.com/actors/monetize/pay-per-event.md)
