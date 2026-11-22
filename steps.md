# Steps: Brand Deal Rate & Usage Rights Calculator (Apify Actor)

Actor name: **BVAL** (display title) / **`bval`** (Actor ID; Apify IDs must be lowercase). Your **team name must match the Actor name** on the submission form, so use "BVAL". Logo: [logo/bval-logo-512.png](logo/bval-logo-512.png) (source: [logo/bval-logo.svg](logo/bval-logo.svg)).

**What it does:** you give it a creator's handle and a brand's deal terms. It returns a fair rate, a breakdown of each add-on (usage, whitelisting, exclusivity), a floor/ask/walk-away range, a verdict on the brand's offer, and a ready-to-send counter-offer email.

**The one rule:** the Actor must be **public on Apify Store and run live** in the 2-minute demo.

**Non-negotiable milestone:** a published, public Actor with **one successful cloud run by 12:00**. Polish comes after that.

---

## Step 0: Lock the basics (before 10:15)

- [x] Actor name: **BVAL**, ID `bval` (lowercase letters, numbers and hyphens only, unique on your account). Check on Console that `bval` is free on the owner account.
- [ ] Buyer persona, written once and reused in the README, Store description and demo:
  - **Primary:** *"Priya, 85k-follower fitness creator in Bengaluru. Acme Protein offered $800 for one Reel plus 90 days paid usage and 6-month category exclusivity. She doesn't know if that's fair or how to push back."*
  - **Secondary (bulk, API buyer):** talent managers and small influencer agencies quoting 10+ deals a week.
- [x] Platforms in scope: **Instagram, TikTok and YouTube (Shorts + long-form videos)**, all first-class. Each platform sells brands something different, so the engine prices each one with its own anchor metric, deliverables and add-ons (see "Platform value propositions" in the research report). Build order, so the 12:00 publish isn't put at risk: Instagram → TikTok → YouTube. Publish as soon as the first platform works and add the others in later builds.
- [ ] Language: **Python** (matches the research report's tooling).

## Step 1: Account and tooling setup (before 10:15, about 20 min)

- [ ] Create an Apify account and apply coupon **`APIFYBLR`** (Console → Billing → Subscription → Add a promo code).
- [ ] On the owner account: **fill in billing and payment details** (the pricing step needs them) and accept the **Store Publishing Terms**.
- [ ] Install tools:
  ```bash
  npm i -g apify-cli
  apify login
  pip install apify
  ```
- [ ] Optional, in Claude Code: `/plugin marketplace add https://github.com/apify/agent-skills`, then `/plugin install apify-actor-development@apify-agent-skills`.
- [ ] Create a **public GitHub repo** with the same name as the Actor (the hackathon asks for a public repo with run instructions).

## Step 2: Check the feeder Actor and save a fixture (10:15–10:30)

We don't write scrapers. We call an existing, well-maintained Store Actor.

- [ ] Instagram: read `https://apify.com/apify/instagram-scraper.md` (append `.md` to any Store URL to get the agent-friendly version). Note the exact input fields (usernames, `resultsLimit`, results type) and the output fields for `videoViewCount` / `videoPlayCount`, `likesCount`, `commentsCount`, `timestamp`, `type`, and the profile's `followersCount`.
- [ ] TikTok (core): `clockworks/tiktok-profile-scraper` with `profiles:[h], resultsPerPage:30, profileSorting:"latest", excludePinnedPosts:true`. Fields: `authorMeta.fans`, `playCount`, `diggCount`, `commentCount`, `shareCount`. ER = (digg + comment + share) / plays. Save a fixture.
- [ ] YouTube (Shorts + long-form): `streamers/youtube-scraper` with `startUrls, maxResults, maxResultsShorts, sortVideosBy:"NEWEST"`. Fields: `numberOfSubscribers`, `viewCount`, `likes`, `commentsCount`, `type`.
- [ ] Full field-level feeder spec: see `reports/BVAL creator rate benchmarks.md`.
- [ ] Run the feeder once from Console on a real public creator, 30 posts, and **save the JSON** as `tests/fixtures/instagram_sample.json`. All local development runs against this file, so we don't spend credits or wait on scrapes.
- [ ] Note how long the run takes and what it costs. That feeds Step 9 (pricing) and the demo plan (runs must stay under about 60s).

## Step 3: Scaffold the Actor (10:30)

```bash
apify create bval -t python-start   # choose "Local only"
cd bval
git init && git remote add origin <github repo url>
```

Target layout:
```
.actor/
  actor.json            # name, title, version, dataset + output schema refs
  input_schema.json
  output_schema.json
  dataset_schema.json   # "overview" table view for the Output tab
src/
  main.py               # orchestration
  scrape.py             # calls the feeder Actor, normalises posts
  metrics.py            # median views, engagement rate, consistency
  pricing.py            # deterministic rate engine (the product)
  pitch.py              # LLM counter-offer email
  config/rates.json     # CPM tables + add-on % (versioned, cited)
tests/fixtures/
README.md
```

## Step 4: Define the input schema (Craft) (10:30–10:50)

Keep it to **at most 8 fields**, each with defaults, prefill, descriptions and enums. Validate with `apify validate-schema`.

| Field | Type | Default / prefill | Notes |
|---|---|---|---|
| `handle` | string | `"natgeo"` (prefill) | Required. Strip any leading `@`. |
| `platform` | enum | `instagram` | `instagram`, `tiktok`, `youtube`. Deliverable options depend on the platform: IG reel/story/static/carousel, TikTok video, YouTube short/integration/dedicated |
| `niche` | enum | `lifestyle` | Sets the base CPM: fitness, beauty, fashion, tech, finance, food, travel, gaming, parenting, lifestyle |
| `deliverables` | array | `[{"type":"reel","count":1}]` | Types: reel, story, static_post, carousel, short_video, long_video |
| `usageRightsDays` | integer | `0` | Organic reuse by the brand |
| `whitelistingDays` | integer | `0` | Paid ads run from the creator's handle |
| `exclusivity` | object | `{"type":"none","days":0}` | Type is `none`, `category` or `full` |
| `brandOffer` | integer (USD) | empty | Optional. Turns on the under/over-market verdict |
| `brandName`, `generatePitch`, `tone` | string / bool / enum | `"", true, "friendly-firm"` | Group these in an "Email" section |

Avoid the removed `patternKey`/`patternValue` properties, which now fail builds.

## Step 5: Build the core logic (10:50–11:30)

### 5a. Scrape and normalise (`scrape.py`)
- [ ] Call the feeder from inside the Actor with `Actor.call("apify/instagram-scraper", run_input=...)`, then read its default dataset.
- [ ] Keep only the last **30 posts**, or the last 90 days, whichever is smaller. Video posts drive the views metrics.
- [ ] Add an `--offline` / fixture mode for local development (read `tests/fixtures/*.json`).

### 5b. Metrics (`metrics.py`)
- [ ] **Median views** of video posts, not the mean, so viral outliers don't inflate the rate.
- [ ] **Engagement rate** = (likes + comments) / views, with followers as a fallback denominator.
- [ ] Posting consistency (posts per week) and a viral-outlier count.
- [ ] Handle the edge cases: private account, no video posts, fewer than 5 posts. Return a clear error item, not a crash.

### 5c. Pricing engine (`pricing.py` + `config/rates.json`). This is the product.
Deterministic and explainable. **No LLM in the number.**
- [ ] `base = medianViews / 1000 × CPM[niche] × deliverableMultiplier[type]`, summed over deliverables.
- [ ] Engagement adjustment: for example ±10–20% when engagement is well above or below the niche benchmark.
- [ ] Add-ons as a percentage of the base, scaled by duration:
  - Usage rights (organic): for example 30 days +15%, 90 days +30%, 180 days +50%, perpetual +100%
  - Whitelisting / paid ads: for example 30 days +30–50%, 90 days +75%
  - Exclusivity: category, for example +20–40% by duration; full, for example +50–100%
  - Rush or extra revisions: optional flat percentages
- [ ] Output a range: `floor` (the base plus add-ons at the low end), `ask` (recommended), `walkAway`.
- [ ] Verdict when `brandOffer` is set: `"65% below market"` / `"fair"` / `"above market"`.
- [ ] Put every number in `rates.json` with a `sources` array and a `version`. Cite public creator-pricing benchmarks, and say in the README that these are benchmarks, not guarantees.
- [ ] Unit-test the engine against 3 hand-calculated cases.

### 5d. Pitch email (`pitch.py`)
- [ ] One LLM call. Use Apify's OpenRouter Actor or proxy (`openrouter.apify.actor`, billed to Apify credit, so no personal API key is needed), as covered in the research report.
- [ ] Prompt inputs: creator metrics, line-item breakdown, brand offer, tone. The email must **cite the numbers** ("my median Reel reaches 42k viewers…") and justify each add-on.
- [ ] Ask for a JSON contract `{subject, body}`. If the LLM fails, fall back to a template email, so the Actor never fails because of the LLM.

## Step 6: Output and dataset schemas (Craft) (11:00–11:30, in parallel)

- [ ] One dataset item per quote:
  ```json
  {
    "handle": "priya.fit", "platform": "instagram", "niche": "fitness",
    "metrics": { "medianViews": 42000, "engagementRate": 4.8, "postsPerWeek": 3.5, "postsAnalyzed": 30 },
    "baseRate": 1050,
    "addOns": [
      { "item": "90-day organic usage", "pct": 30, "amount": 315 },
      { "item": "30-day whitelisting", "pct": 50, "amount": 525 },
      { "item": "180-day category exclusivity", "pct": 40, "amount": 420 }
    ],
    "rateRange": { "floor": 1850, "ask": 2310, "walkAway": 1600 },
    "brandOffer": 800, "verdict": "65% below market",
    "pitchEmail": { "subject": "...", "body": "..." },
    "rateCardVersion": "2026-11-22", "currency": "USD"
  }
  ```
- [ ] `dataset_schema.json`: a **"Quote summary" table view** (handle, median views, ER, ask, offer, verdict).
- [ ] `output_schema.json` (**required for publishing**): link to the dataset view, plus a **Markdown quote report** saved to the key-value store (`QUOTE.md`), so the Output tab looks like a finished deliverable.
- [ ] `apify validate-schema`.

## Step 7: Run locally, push, and do the first cloud run (11:30–11:45)

```bash
apify run -p -i '{"handle":"<creator>","niche":"fitness","deliverables":[{"type":"reel","count":1}],"usageRightsDays":90,"whitelistingDays":30,"exclusivity":{"type":"category","days":180},"brandOffer":800,"brandName":"Acme Protein"}'
apify push        # builds on the platform
```
- [ ] Run it once in Console. **Publishing needs at least one successful run.**
- [ ] Check the Output tab: the table view renders and `QUOTE.md` opens.

## Step 8: Publish on the Store, even if rough (11:45–12:00)

Console → My Actors → `bval` → **Publishing** tab:
- [ ] Display information: title ("BVAL: Brand Deal Rate Calculator for Creators"), short description (persona plus the outcome), logo/icon: upload [logo/bval-logo-512.png](logo/bval-logo-512.png).
- [ ] Categories: **AI**, **Social media**, and possibly **Lead generation / Business**.
- [ ] Sample output (from the successful run).
- [ ] Output schema attached.
- [ ] Permissions: **limited**. Full permissions trigger identity verification.
- [ ] Monetization: **pay-per-event** (Step 9). Do **not** turn on "PPE + usage", which takes 14 days.
- [ ] Click **Publish on Store**, then copy the **direct Store URL**. New low-usage Actors may not show up in Store search, so give judges the URL.

Things that could block publishing: no successful run, missing output schema, missing billing details, full permissions, or the PPE + usage toggle.

## Step 9: Pricing model, pay-per-event (Craft)

| Event | Price | When charged |
|---|---|---|
| `apify-actor-start` | platform default | each run |
| `creator-analyzed` | **$0.05** | once per handle scraped and analysed (covers the feeder cost) |
| `quote-generated` | **$0.25** | once per rate quote |
| `pitch-email-generated` | **$0.25** | only if `generatePitch` is true |

- [ ] Fill in the real costs from Step 2 (feeder cost per 30 posts, LLM cost per email, compute) and check the margin. You keep 80% of revenue minus platform costs, so aim for at least 3x.
- [ ] Charge in code with `await Actor.charge(event_name="quote-generated")` and so on, **after** each step succeeds.
- [ ] Turn off the synthetic per-dataset-item event, so buyers are charged only the named events.
- [ ] Pitch line for the README and demo: *"A $0.55 quote that can add $1,000+ to one deal."* Agencies quoting 50 deals a month pay about $27.

## Step 10: README that sells (13:00–13:45)

1. **Hero line:** "Know what to charge before you reply to a brand. Rates, usage rights and a counter-offer email in 30 seconds."
2. **Who it's for:** Priya (creator) and agencies/talent managers.
3. **The problem:** whitelisting, usage and exclusivity terms quietly devalue deals.
4. **What you get:** a screenshot of the Output tab, the line-item breakdown, the verdict, and the email.
5. **How it works:** a 4-step diagram: public posts via `apify/instagram-scraper` → metrics → deterministic pricing engine → LLM email. Explain the formula and add-on percentages openly.
6. **Input:** a field table and an example JSON.
7. **Sample output:** the JSON plus the rendered `QUOTE.md`.
8. **Pricing:** the event table, worked examples, and how to cap spend with a maximum total charge.
9. **Integrations:** call it via API, MCP or AI agents, Make/Zapier/n8n, or schedule it for agency rosters.
10. **FAQ and limits:** public data only, benchmarks rather than financial advice, USD only, supported platforms.
11. **Run locally:** `apify run` instructions (required by the hackathon).

Mirror the README in the public GitHub repo.

## Step 11: Polish, if time allows (13:00–14:10)

In priority order. Stop when you reach 14:10.
1. [ ] Markdown `QUOTE.md` report that's nice enough to screenshot.
2. [ ] Error handling: private account, bad handle, feeder timeout. Each returns a friendly error item, and no charge for failed steps.
3. [ ] INR output option (Bengaluru judges will relate to it).
4. [ ] Finish whichever platforms (TikTok / YouTube) didn't make the first publish.
5. [ ] Batch mode: an array of handles for agencies.

**Cut-scope fallback, in order:** drop extra platforms → drop INR → drop batch → if the LLM breaks, ship the template email. The pricing breakdown on its own is still a conclusion.

## Step 12: Final verification (14:10–14:20)

- [ ] `apify push` the final build.
- [ ] Run it 3 times from the **public Store page**, logged in, on 3 different creators. Each run should finish in under 60s with correct charges.
- [ ] Check the Output tab, `QUOTE.md`, the README rendering and the pricing display on the Store page.
- [ ] Freeze the code. Push the repo to GitHub.

## Step 13: Demo prep (14:20–14:30) and submit

- [ ] Pre-run a **backup run** with the exact demo input and keep it open in a tab.
- [ ] 2-minute script (rehearse twice with a timer):
  - **0:00–0:15, buyer:** "Priya got $800 for a Reel plus 90 days of ads plus exclusivity. Is that fair?"
  - **0:15–0:25, live run:** open the public Store page, paste the input, click Start. "Live on Apify Store."
  - **0:25–0:55, while it runs:** "We call Apify's Instagram Scraper for real median views. The rate comes from a transparent pricing engine, not a guess. The LLM only writes the email."
  - **0:55–1:35, output:** "Fair ask is $2,310. Her offer is 65% below market. Here's what each add-on is worth, and here's the counter-offer email, ready to send."
  - **1:35–1:50, money:** "$0.55 per quote, pay-per-event. Agencies run it for whole rosters through the API or MCP."
  - **1:50–2:00, close:** "Know your worth before you reply." If the run is still going at 0:55, switch to the backup tab.
- [ ] Fill in the **Google Form** (shared on the day). Team name = Actor name, Store URL, GitHub URL.
- [ ] Optional: post on LinkedIn or X tagging **@apify**.

---

### Reference docs
[CLI quick start](https://docs.apify.com/cli/docs/quick-start.md) · [CLI reference](https://docs.apify.com/cli/docs/reference.md) · [actor.json](https://docs.apify.com/actors/development/actor-definition/actor-json.md) · [Input schema spec](https://docs.apify.com/actors/development/actor-definition/input-schema/specification/v1.md) · [Output schema](https://docs.apify.com/actors/development/actor-definition/output-schema.md) · [Dataset schema](https://docs.apify.com/storage/dataset-schema.md) · [Calling other Actors (Python)](https://docs.apify.com/sdk/python/docs/concepts/interacting-with-other-actors.md) · [Publish](https://docs.apify.com/actors/publishing/publish.md) · [Monetization](https://docs.apify.com/actors/monetize/set-up-monetization.md) · [Pay-per-event](https://docs.apify.com/actors/monetize/pay-per-event.md) · [Quality score](https://docs.apify.com/actors/publishing/quality-score.md)
