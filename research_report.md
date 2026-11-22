# AI Tools that Earn: Actor Idea Research and Build Plan

*Prepared 22 Nov 2026 (hackathon day). The Store figures are what the Apify Store API and Actor pages showed on 2026-11-22. Monthly users / total users are 30-day and all-time. Ratings show stars and the number of reviews.*

---

## 1. Executive summary

**Recommended Actor: ReviewRx.** You give it Google Maps URLs for restaurants or clinics. It returns a weekly action brief for each one:
- a reputation health score from 0 to 100
- the top 3 issues, each with quoted evidence and the share of reviews that mention it
- 3 fixes to make this week
- ready-to-post replies to the worst recent reviews
- an optional benchmark against nearby competitors

**Buyer.** Operations or marketing managers at multi-outlet restaurant and clinic chains. The concrete example is the ops head of a Bengaluru group with 3 to 10 cafés. Local digital-marketing agencies that manage reputation for 10 to 50 SMB clients are the second buyer. Today someone on that team reads hundreds of reviews by hand every week. ReviewRx turns them into a one-page to-do list.

**What they pay for.** About $0.49 per brief per location, using pay-per-event pricing. That replaces roughly an hour of reading per outlet per week.

**Why this one wins on the four criteria.**
- **Buyer.** Reputation tools are an established paid category. Judges can picture a café owner in Whitefield immediately.
- **Output.** The result is a score and a to-do list, not a review dump.
- **Shipped.** It needs one call to an existing Actor plus one LLM call. That Actor is [compass/Google-Maps-Reviews-Scraper](https://apify.com/compass/Google-Maps-Reviews-Scraper), with 10,005 monthly users and a 4.9 rating from 198 reviews. A live run fits in under 60 seconds.
- **Craft.** The input schema is small and clean. The README sells itself with a before/after picture.

**The gap is real.** The raw review scraper is heavily used. The only Google-Maps review analyzers on the Store are stale and unused:
- [architjn/google-maps-review-ai-summariser](https://apify.com/architjn/google-maps-review-ai-summariser): 0 monthly users, last modified 2 Apr.
- [skunkattack/google-maps-review-sentiment-analyzer](https://apify.com/skunkattack/google-maps-review-sentiment-analyzer): 1 monthly user, last modified 29 Jan.

**Alternatives, in order.**
1. **Hiring-Intent Brief.** Job posts become a ranked list of accounts that are buying now. Higher value per buyer, but the data sources carry terms-of-service risk.
2. **India Funding Radar.** Indian startups that raised this month, with a fit score and an outreach opener. It matches the organiser's own example, so expect other teams to build it too. It also needs a longer chain of steps.

**Nothing found blocks a same-day publish.** No review step is documented. The 14-day monetization notice does not apply while an Actor has no paying users.

---

## 2. What each judging criterion requires

The idea must pass every check below before the demo.

| Criterion | Check |
|---|---|
| **Buyer** | The README and the first 10 seconds of the demo name a specific role in a specific organisation, plus why they need this weekly. ReviewRx: "ops head of a multi-outlet café chain" and "reputation agency". |
| **Output** | Every dataset row contains a decision: a score, ranked issues and actions. Raw reviews are never the deliverable. They appear only as evidence quotes. |
| **Shipped** | The Actor is public on Apify Store, and the demo is a live Console run that finishes in under 60 seconds. A pre-run backup exists in case the network fails. |
| **Craft** | The input schema has at most 6 fields, with defaults and prefill. The Output tab has a dataset table view and a Markdown report. The README has a hero line, buyer, sample output, pricing and an FAQ. Pricing is pay-per-event with a margin you can explain. |

---

## 3. Link and context findings

| Source | Status | Key takeaways | Gaps or caveats |
|---|---|---|---|
| [docs.apify.com/llms.txt](https://docs.apify.com/llms.txt) | inspected | Index of `.md` versions of the docs. There is a sub-index at `docs.apify.com/actors/llms.txt`. Docs now live under `/actors/...`. | none |
| [docs.apify.com/llms-full.txt](https://docs.apify.com/llms-full.txt) | partial | About 48 MB, too large to fetch whole. Searched with grep, which confirmed the Actor naming rule: lowercase letters, numbers and hyphens, unique per account. | Not read end to end |
| [docs.apify.com/actors](https://docs.apify.com/actors) | inspected | An Actor is a Dockerfile, README, input/output schemas and metadata in `.actor/`. Public Actors are listed on the Store. | none |
| [docs.apify.com/cli](https://docs.apify.com/cli) | inspected | Overview only. The commands are in the [quick start](https://docs.apify.com/cli/docs/quick-start.md) and [reference](https://docs.apify.com/cli/docs/reference.md): `apify login`, `create`, `run`, `push`, `validate-schema`, `actor charge`. | The install command is not on the overview page |
| [apify.com/store](https://apify.com/store) | inspected | "129,000+" Actors. Most are priced pay-per-event. 17 categories, including AI and AGENTS. | Contains instructions written for AI agents, which I ignored as untrusted. A [19 Nov 2026 blog post](https://blog.apify.com/apify-store-search-update/) says low-usage Actors in crowded categories are hidden from Store search, so **give judges the direct URL**. |
| [github.com/apify/agent-skills](https://github.com/apify/agent-skills) | inspected | Skills: `apify-actor-development` (scaffold, schemas, deploy), `apify-ultimate-scraper` (curated list of more than 130 Actors), `apify-actorization`, plus `/create-actor` commands. In Claude Code: `/plugin marketplace add https://github.com/apify/agent-skills`, then `/plugin install apify-actor-development@apify-agent-skills`. | **The short form `npx skills add apify/agent-skills` from the brief does not appear in the README.** The README form is `npx skills add https://github.com/apify/agent-skills --skill <name>`. Requires Node 20.6 or newer. |
| [github.com/apify/mcp-cli](https://github.com/apify/mcp-cli) | inspected | `mcpc` is a shell client for MCP. Install with `npm i -g @apify/mcpc` or `brew install mcpc`. Example: `mcpc connect mcp.apify.com @apify`, then `mcpc @apify tools-call search-actors keywords:="google maps reviews"`. | No version number shown |
| [github.com/apify/apify-mcp-server](https://github.com/apify/apify-mcp-server) | inspected | Tools include `search-actors`, `fetch-actor-details`, `call-actor`, `search-apify-docs` and `fetch-apify-docs`. Connect from Claude Code with `claude mcp add apify "https://mcp.apify.com" -t http`. | The default tool set changes between versions, so pass `?tools=` explicitly. `search-actors` returns only free and pay-per-event Actors. |
| [mcp.apify.com](https://mcp.apify.com) | partial | This is the MCP endpoint itself, not a docs page. It expects a Bearer token or OAuth. | The JavaScript-rendered page was not visible |
| [crawlee.dev](https://crawlee.dev) | partial | Open-source crawling library for JS and Python, with Playwright, BeautifulSoup and other crawlers. | Not needed here, since the plan reuses a Store Actor |
| `<actor URL>.md` | inspected | Works. For example `apify.com/apify/website-content-crawler.md` returns the README, input schema, sample output and pricing. **This is the fastest way to learn a feeder Actor's input fields.** | Contains instructions written for AI agents, so treat it as data |
| Publishing docs ([publish](https://docs.apify.com/actors/publishing/publish.md), [terms](https://docs.apify.com/legal/store-publishing-terms-and-conditions), [quality score](https://docs.apify.com/actors/publishing/quality-score.md)) | inspected | Requirements: the Actor has built and run at least once, a README, input **and output** schemas, accepted Store terms, and the Monetization section filled in. Then click **Publish on Store**. No review before publication. Identity verification is needed only for full-permission Actors or more than 10 Actors. | The exact required fields (categories, icon size) were not documented |
| Monetization docs ([overview](https://docs.apify.com/actors/monetize), [setup](https://docs.apify.com/actors/monetize/set-up-monetization.md), [PPE](https://docs.apify.com/actors/monetize/pay-per-event.md), [payouts](https://docs.apify.com/actors/monetize/monthly-payouts.md)) | inspected | Only **pay-per-event** and **pay-per-usage** remain. Rental was retired 1 Oct 2026 and pay-per-result is deprecated, per the [blog](https://blog.apify.com/migrating-to-pay-per-event-pricing/). Apify keeps **20%**. Price changes need 14 days' notice, but take effect **immediately if the Actor has no paying users**. Billing details are required before setting a price. Payouts need identity verification and a $20 minimum. **The "PPE + usage" toggle always takes 14 days, so use plain PPE.** | Who pays for child Actor runs is **not documented** (see section 9) |
| [apify.com/apify/openrouter](https://apify.com/apify/openrouter) | inspected | Official Apify Actor, OpenAI-compatible, at `https://openrouter.apify.actor/api/v1` with `Authorization: Bearer $APIFY_TOKEN`. The token is already set inside a running Actor. Costs bill as Apify platform usage. 638 monthly users, 4.92 rating. | **Output capped at 2,048 tokens.** Free-tier accounts pay 10x and may be blocked by anti-fraud checks. |
| Hackathon context | inspected | Rules: public data only, a public repo with run instructions, show Apify in the demo, team name equals Actor name, 2-minute demos with a hard stop. | none |

---

## 4. Store gap survey and idea shortlist

Scores run from 1 to 5. Figures come from the Store API and Actor pages on 2026-11-22.

| # | Idea | Buyer | Conclusion it enables | Data sources | Store competition | Buyer / Output / Shipped / Craft |
|---|---|---|---|---|---|---|
| **1** | **ReviewRx**: Google reviews become a weekly action brief | Ops head of a multi-outlet restaurant or clinic chain; SMB reputation agencies | What to fix this week, which reviews to reply to, and how we compare with competitors | [compass/Google-Maps-Reviews-Scraper](https://apify.com/compass/Google-Maps-Reviews-Scraper) (10,005 / 71,555 users, 4.9 from 198 reviews, $0.0006/review); optional [compass/crawler-google-places](https://apify.com/compass/crawler-google-places) for competitors (48,926 monthly users, 4.7 from 1,820 reviews) | The analyzers are stale or unused: [architjn summariser](https://apify.com/architjn/google-maps-review-ai-summariser) (0 monthly users), [skunkattack sentiment](https://apify.com/skunkattack/google-maps-review-sentiment-analyzer) (1). [ryanclinton/trustpilot-review-analyzer](https://apify.com/ryanclinton/trustpilot-review-analyzer) covers Trustpilot only (2 monthly users, $0.15/business). | **4 / 5 / 5 / 5** |
| 2 | **Hiring-Intent Brief**: companies hiring role X become accounts buying now | SDR lead at a B2B SaaS company selling dev tools, HR tech or cloud services; staffing agencies | Which 20 accounts to call this week, why now, and an opening line | [curious_coder/linkedin-jobs-scraper](https://apify.com/curious_coder/linkedin-jobs-scraper) (13,432 monthly), [muhammetakkurtt/naukri-job-scraper](https://apify.com/muhammetakkurtt/naukri-job-scraper) (918 monthly), [valig/indeed-jobs-scraper](https://apify.com/valig/indeed-jobs-scraper) | Almost no conclusion layer: [constructive_calm/ats-hiring-intent-scraper](https://apify.com/constructive_calm/ats-hiring-intent-scraper) (0 monthly, US/EU ATS boards), [tribloc/company-hiring-signals](https://apify.com/tribloc/company-hiring-signals) (6 monthly). Nothing for India. | **5 / 5 / 4 / 4**. ⚠ LinkedIn's terms forbid scraping; Naukri's terms likely forbid automated access too (not verified). |
| 3 | **India Funding Radar**: this month's Indian funding rounds become fit-scored leads with an opener | Sales team at a B2B SaaS company or agency selling to newly funded startups (the organiser's own example) | Which newly funded startups to contact first and what to say | Entrackr `news-sitemap.xml` (its robots.txt is permissive), Google News RSS (personal feed-reader use only, a grey area), [nexgendata/india-startup-funding-tracker](https://apify.com/nexgendata/india-startup-funding-tracker), a contact scraper | Raw Crunchbase scrapers ([memo23](https://apify.com/memo23/crunchbase-scraper), 180 monthly). The only India tracker has 1 monthly user and no scoring. [scrapemint funded-startup pipeline](https://apify.com/scrapemint/funded-startup-lead-pipeline) is US SEC data only. | **5 / 5 / 3 / 4**. Other teams will likely pick it. ⚠ Inc42's and YourStory's robots.txt signals restrict AI use. |
| 4 | **Vendor Due-Diligence Brief (India)** | Credit or procurement team at an NBFC or lender | Approve, review or reject the vendor | MCA Actors ([thirdwatch/mca-india-scraper](https://apify.com/thirdwatch/mca-india-scraper)), GSTIN ([mikolabs/gstin](https://apify.com/mikolabs/gstin)), WHOIS, news | [ryanclinton/company-deep-research](https://apify.com/ryanclinton/company-deep-research) is US-centric with 2 monthly users | **5 / 5 / 2 / 3**. The MCA and GST portals use captchas, and a 4–5 source chain is fragile in a live demo. |
| 5 | **App Review to Roadmap** | Product manager at a consumer app | The next sprint's top bugs and features | [thewolves Play](https://apify.com/thewolves/google-play-reviews-scraper) and [App Store](https://apify.com/thewolves/appstore-reviews-scraper) review scrapers | [yasaslive/app-review-intel](https://apify.com/yasaslive/app-review-intel) already does it (1 monthly, needs the buyer's own OpenAI key) | **4 / 4 / 5 / 4**. Judges may see it as already done. |
| 6 | **Local Lead Scorer for agencies** | Web or SEO agency | Which SMBs to pitch | Google Maps plus a website check | Built at least 5 times: [ryanclinton/lead-scoring-engine](https://apify.com/ryanclinton/lead-scoring-engine), [jurassic_jove/website-audit-leads](https://apify.com/jurassic_jove/website-audit-leads), [latentlark/local-lead-audit](https://apify.com/latentlark/local-lead-audit) and others | **4 / 4 / 4 / 3**. Looks derivative. |
| 7 | **AI-Search Readiness Audit / Pricing Monitor** | Marketing lead | What to fix for AI search visibility | Website crawl | Crowded: 277 Store results for "AI search readiness", 630 for "GEO audit" ([fayoussef](https://apify.com/fayoussef/seo-geo-aeo-audit), [foxlabs](https://apify.com/foxlabs/geo-auditor) and others) | **3 / 4 / 4 / 3** |

**Comparing the top three**

| | ReviewRx | Hiring-Intent | Funding Radar |
|---|---|---|---|
| Buyer clarity | High: owners and agencies | Very high: SDR teams | Very high: sales teams |
| Willingness to pay | Proven category: Birdeye, ReviewTrackers and similar | High: intent data is a paid category | High |
| 3.25-hour feasibility | One Actor call plus one LLM call | One Actor call, a grouping step, then the LLM | News source, LLM extraction, then enrichment |
| Live demo under 60s | Yes, with about 80 reviews and no benchmark | Likely | Risky, because enrichment adds latency |
| Data and terms risk | Medium: Google Maps scraping is Apify's most-used category but sits in a terms grey zone; reviews are public | **High**: LinkedIn and Naukri terms | Medium: news sites' robots.txt signals |
| Store competition | Stale or unused | Near zero | Low, but other hackathon teams |

---

## 5. Recommended solution (primary): ReviewRx

### Architecture
- **Language:** Python. Use the `python-start` template from `apify create`, with the Apify Python SDK and the `openai` client.
- **Flow:**
  1. `Actor.get_input()`
  2. `Actor.call('compass/Google-Maps-Reviews-Scraper', ...)` once for all place URLs
  3. Group reviews by place
  4. Compute the score in code:
     - star average for the period
     - share of 1–2★ reviews
     - recent-versus-earlier trend
     - share of negative reviews left unanswered by the owner
  5. One LLM call per place through `apify/openrouter`, asking for strict JSON:
     - issue clusters with evidence quotes
     - 3 actions for this week
     - 3 reply drafts
     - what guests love
  6. Build the Markdown brief
  7. `Actor.push_data()` one row per place
  8. Save `BRIEF.md` (or `.html`) to the key-value store
  9. `Actor.charge('brief-generated')`
- **Optional competitor benchmark:** call `compass/crawler-google-places` with `searchStringsArray` set to the business type plus the area, and 3 places. Then compare rating, review count and top themes. **Leave it off by default and out of the live demo.**
- **Why the score is computed in code:** it is deterministic and explainable ("score = 40% rating, 25% negative share, 20% trend, 15% response rate"). That makes it believable to judges. The LLM handles only the language-heavy parts.
- **LLM output limit:** keep JSON compact, because output is capped at 2,048 tokens. Send at most about 120 reviews, truncated to 300 characters each.

### Skeleton (`src/main.py`)

Verify the feeder input field names against `https://apify.com/compass/Google-Maps-Reviews-Scraper.md` before you rely on them.

```python
import os, json
from apify import Actor
from openai import AsyncOpenAI

async def main():
    async with Actor:
        inp = await Actor.get_input() or {}
        urls = [u["url"] if isinstance(u, dict) else u for u in inp["placeUrls"]]
        run = await Actor.call("compass/Google-Maps-Reviews-Scraper", run_input={
            "startUrls": [{"url": u} for u in urls],
            "maxReviews": inp.get("maxReviews", 80),
            "reviewsSort": "newest",            # verify field names in the .md page
            "language": "en",
        })
        items = (await Actor.apify_client.dataset(run.default_dataset_id).list_items()).items
        llm = AsyncOpenAI(base_url="https://openrouter.apify.actor/api/v1",
                          api_key=os.environ["APIFY_TOKEN"])
        for place, reviews in group_by_place(items).items():
            metrics = score(reviews)                      # deterministic 0-100
            resp = await llm.chat.completions.create(
                model=inp.get("model", "<openrouter model slug>"),
                response_format={"type": "json_object"},
                max_tokens=1800,
                messages=[{"role": "system", "content": SYSTEM_PROMPT.format(biz=inp.get("businessType","restaurant"))},
                          {"role": "user", "content": compact(reviews)}])
            brief = json.loads(resp.choices[0].message.content)
            row = build_row(place, metrics, brief)
            await Actor.push_data(row)
            await Actor.set_value(f"brief-{row['placeSlug']}", row["briefMarkdown"], content_type="text/markdown")
            await Actor.charge(event_name="brief-generated")
```

### Input schema (`.actor/input_schema.json`), 6 fields

| Field | Type / editor | Default and prefill | Notes |
|---|---|---|---|
| `placeUrls` | array / `requestListSources` | prefill: one Bengaluru café URL | Required. One brief per place. |
| `businessType` | string / `select` | `restaurant` | Options: restaurant, cafe, clinic, hotel, salon, retail. Tunes the issue categories. |
| `maxReviews` | integer | default 80, min 20, max 300 | Most recent first. Controls speed and cost. |
| `includeCompetitorBenchmark` | boolean | false | Under a section caption "Benchmark (slower)". Charged as a separate event. |
| `replyTone` | string / `select` | `warm-professional` | Options: warm-professional, formal, casual. |
| `outputLanguage` | string / `select` | `en` | Options: en, hi. A cheap differentiator for India. |

### Output dataset, one row per place

The dataset schema `overview` view shows these columns: place, healthScore, trend, topIssue, actionsThisWeek and briefUrl.

```json
{
  "placeName": "Third Wave Coffee, Whitefield",
  "placeUrl": "https://maps.google.com/?cid=…",
  "periodAnalyzed": "2026-09-24 → 2026-11-21",
  "reviewsAnalyzed": 80,
  "avgRating": 4.1,
  "healthScore": 68,
  "trend": "declining (-0.4★ vs previous 40 reviews)",
  "unansweredNegativeShare": 0.62,
  "topIssues": [
    {"issue": "Slow service at weekend peak", "share": 0.21, "severity": "high",
     "evidence": ["Waited 25 min for a cold brew on Saturday", "…"],
     "fix": "Add one barista 10am–2pm Sat/Sun; pre-batch cold brew"},
    {"issue": "Wi-Fi drops for remote workers", "share": 0.12, "severity": "medium", "evidence": ["…"], "fix": "…"},
    {"issue": "Pricing vs portion size", "share": 0.09, "severity": "low", "evidence": ["…"], "fix": "…"}
  ],
  "whatGuestsLove": ["Pour-over quality", "Quiet upstairs seating"],
  "actionsThisWeek": [
    "Roster an extra barista for weekend peak",
    "Reply to the 5 unanswered 1–2★ reviews (drafts below)",
    "Put Wi-Fi password + reset instructions on table cards"
  ],
  "replyDrafts": [{"stars": 1, "reviewExcerpt": "Waited 25 min…", "draft": "Hi Priya, you're right that…"}],
  "competitorBenchmark": null,
  "briefMarkdown": "# Weekly Review Brief — Third Wave Coffee, Whitefield\n…",
  "briefUrl": "https://api.apify.com/v2/key-value-stores/…/records/brief-third-wave-whitefield"
}
```

The values above are an illustrative mock. Real runs fill them from live reviews.

The output schema (`.actor/output_schema.json`, required for Store publishing) should have two properties:
- `briefs` pointing to `{{links.apiDefaultDatasetUrl}}/items`
- `report` pointing to the key-value store record

### Evidence and rationale
- **Strong feeder Actor.** It is reliable and cheap: 10,005 monthly users, 4.9 rating, $0.0006 per review. That makes a live demo low-risk and 80 reviews cost about $0.05.
- **No live competitor.** No maintained conclusion-layer Actor exists for Google reviews. The two analyzers have 0–1 monthly users and were last modified in January and April 2026.
- **LLM billed to Apify credit.** `apify/openrouter` bills to Apify, so there are no extra API keys or accounts, and the demo shows more of Apify.
- **Relatable to judges.** You can run it live on a café near Zostel Plus Whitefield.

### Trade-offs and risks
- **Google terms.** Google's terms restrict scraping Maps. This is Apify's most-used category and the reviews are public, but say "public reviews via an existing Store Actor" and avoid personal data. Reviewer names appear only inside reply drafts, and you can drop them with a flag.
- **Run time.** The feeder Actor's start-up time plus scraping adds latency. Keep `maxReviews` at 80, the benchmark off, and test the timing at 11:30. If a run takes more than 60s, drop to 50 reviews.
- **LLM output.** It may return invalid JSON. Use `response_format`, one retry, and fall back to a brief without reply drafts.
- **Pricing comparison.** The Trustpilot analyzer charges $0.15 per business. Justify a higher price by the action layer and reply drafts, or price lower (see section 7).

## 6. Alternatives

**A. Hiring-Intent Brief.** Use this if your team includes a sales or B2B person who can tell the buyer story.
- **Input:** role keywords such as "DevOps engineer, Kubernetes", a location, and the product being sold.
- **Flow:** Indeed scraper ([valig](https://apify.com/valig/indeed-jobs-scraper), lowest terms risk of the job sources), group by company, compute signals in code (posting count, seniority, recency, tech keywords), then an LLM writes a 2-line "why now" and an opener for each account. The output is a ranked list of 20 accounts.
- **Pricing:** $0.05 per qualified account.
- **Main risk:** the source sites' terms. LinkedIn explicitly forbids scraping. Naukri likely does too (not verified).

**B. India Funding Radar.** Choose it only if you're confident other teams aren't building it.
- **Input:** time window, sector filter, and your ICP description.
- **Flow:** Entrackr news sitemap plus Google News RSS, LLM extraction of startup, amount, round, investors and sector, an ICP fit score, then optionally [delicious_zebu/contact-info-scraper](https://apify.com/delicious_zebu/contact-info-scraper) on the company websites for public contact emails.
- **Pricing:** $0.10 per scored lead, $0.05 extra with contacts.
- **Main risks:** enrichment latency, and duplicating the organiser's example.

---

## 7. Build and ship plan

### Before 10:15 (do it at the venue while people settle in)

This setup takes 15–20 minutes, and if it fails the whole build stalls.
1. Each member creates an Apify account and applies coupon `APIFYBLR`. Pick **one** account to own the Actor.
2. On the owner account, fill in **billing and payment details**, which pricing setup requires, and accept the **Store Publishing Terms**.
3. Install the tools:
   - `npm i -g apify-cli`, then `apify login`
   - `pip install apify openai` (local dev)
   - optionally `claude mcp add apify "https://mcp.apify.com" -t http`
4. In Claude Code: `/plugin marketplace add https://github.com/apify/agent-skills`, then `/plugin install apify-actor-development@apify-agent-skills`.
5. Create a public GitHub repo named after the Actor.

### Timeline

| Time | Work | Owner |
|---|---|---|
| 10:15–10:30 | `apify create reviewrx -t python-start`. Read `https://apify.com/compass/Google-Maps-Reviews-Scraper.md` for the exact input and output fields. Run the feeder once from Console on a Whitefield café and save the JSON as a test fixture. | All |
| 10:30–11:15 | **A:** feeder call, group-by-place, deterministic score. **B:** LLM prompt and JSON contract, tested against the fixture through `openrouter.apify.actor`. **C:** `input_schema.json`, `output_schema.json`, dataset schema `overview` view, then `apify validate-schema`. | Split |
| 11:15–11:45 | Wire it end to end and test with `apify run -p`. Then **`apify push`** and do the first cloud run. *Publishing requires at least one successful run, so get it early.* | A + B |
| 11:45–12:00 | **Publish now, even if rough.** Publishing tab: title, description, icon, categories (AI, Lead generation / Business), limited permissions, PPE pricing. Click Publish on Store. | C |
| 12:00–13:00 | Lunch. One person times cloud runs and tunes `maxReviews` to keep them under 60s. | — |
| 13:00–13:45 | Polish: Markdown brief, reply drafts, Hindi option, error handling and retry. Write the README (see the outline below). Add `Actor.charge`. | Split |
| 13:45–14:10 | Optional benchmark flag (**skip if behind**). Push the final build and run it 3 times on different places. | A |
| 14:10–14:30 | Rehearse the demo twice with a timer. Pre-run a backup run and keep it open in a tab. Fill in the repo README run instructions. Freeze the code. | All |

**Cut-scope fallback, in order:**
1. Drop the competitor benchmark.
2. Drop the Hindi output.
3. Drop the reply drafts and keep the score, issues and 3 actions.
4. If the LLM path breaks, ship the deterministic score plus top negative keywords and evidence quotes. That still counts as a conclusion.

**The non-negotiable:** a published, public Actor with one successful run by 12:00.

### Publish steps (exact)
```bash
apify login                           # browser or --token <token>
apify create reviewrx -t python-start # choose "Local only"
cd reviewrx
apify run -p -i '{"placeUrls":[{"url":"<maps url>"}],"maxReviews":50}'
apify validate-schema
apify push                            # builds on platform; then run once in Console
```
Then in Console, go to My Actors, open reviewrx, then the **Publishing** tab:
- Display information: title, description and logo
- Sample output
- Output schema (required)
- Monetization: pay-per-event
- Permissions: limited

Then click **Publish on Store**.

Docs: [CLI quick start](https://docs.apify.com/cli/docs/quick-start.md), [CLI reference](https://docs.apify.com/cli/docs/reference.md), [actor.json](https://docs.apify.com/actors/development/actor-definition/actor-json.md), [input schema spec](https://docs.apify.com/actors/development/actor-definition/input-schema/specification/v1.md), [output schema](https://docs.apify.com/actors/development/actor-definition/output-schema.md), [dataset schema](https://docs.apify.com/storage/dataset-schema.md), [calling other Actors (Python)](https://docs.apify.com/sdk/python/docs/concepts/interacting-with-other-actors.md), [publish](https://docs.apify.com/actors/publishing/publish.md), [set up monetization](https://docs.apify.com/actors/monetize/set-up-monetization.md), [pay-per-event](https://docs.apify.com/actors/monetize/pay-per-event.md), [quality score](https://docs.apify.com/actors/publishing/quality-score.md).

**Things that could block publishing:**
- No successful run yet.
- Missing output schema.
- Billing details missing, which blocks the pricing step.
- Requesting full permissions, which triggers identity verification.
- Using the "PPE + usage" toggle, which takes 14 days.
- The removed `patternKey`/`patternValue` input schema properties, which now fail builds.

**Discoverability:** new low-usage Actors may not appear in Store search, so give judges the **direct URL**.

### Pricing model: pay-per-event
| Event | Price | Reasoning |
|---|---|---|
| `apify-actor-start` (synthetic) | default $0.00005 | Platform default |
| `brief-generated` (per place) | **$0.49** | Estimated cost per brief: about $0.05 for 80 reviews at $0.0006 each, roughly $0.01–0.03 of LLM, about $0.01 of compute, so about $0.10. The creator keeps 80% × $0.49 − $0.10 ≈ $0.29, about 3x margin. A weekly brief for 10 outlets costs about $20/month, far cheaper than a SaaS reputation subscription and much cheaper than an hour of manager time per outlet. |
| `competitor-benchmark` (per place) | $0.25 | Covers the extra Google Maps search plus a premium |

- **Why PPE:** rental is retired and pay-per-result is deprecated. PPE is also the model buyers see across the Store.
- **No extra wait:** the price applies immediately because the Actor has no paying users yet.
- **Turn off the synthetic per-dataset-item event** so buyers are charged only `brief-generated`.
- Mention in the README that users can cap spend with a maximum total charge.

### README outline
1. **Hero line:** "Turn 300 Google reviews into a 1-page Monday to-do list, for $0.49 per outlet."
2. **Who it's for:** ops heads of multi-outlet restaurant, café and clinic chains, and reputation or marketing agencies.
3. **What you get:** health score, top issues with evidence, 3 actions this week, reply drafts, and the optional benchmark. Include a screenshot of the Output tab.
4. **How it works:** a 3-step diagram. Public Google reviews via the Store Actor compass/Google-Maps-Reviews-Scraper, then deterministic scoring, then an LLM brief via Apify OpenRouter. Explain the score formula.
5. **Input:** a table of the 6 fields and an example JSON.
6. **Sample output:** a JSON record plus the rendered Markdown brief.
7. **Pricing:** the event table, worked examples ("10 outlets weekly ≈ $20/month"), and how to cap spend.
8. **Use cases:** a weekly schedule with a Slack or email integration, an agency client report, and comparing locations.
9. **FAQ and limits:** public data only, supported languages, review count limits, data handling.
10. **Run locally:** `apify run` instructions (the hackathon requires them in the repo).

### 2-minute demo script

Two people: a driver and a speaker. Start a timer.

- **0:00–0:15, the buyer.** "Meet Ravi. He runs ops for a 6-outlet café chain in Bengaluru. Every Monday he reads hundreds of Google reviews to decide what to fix. That's 5 hours of reading for 3 decisions."
- **0:15–0:25, the live run.** Driver opens the **public Store page** of ReviewRx, pastes the Maps URL of a café near this venue, sets 80 reviews, clicks **Start**. "This is live on Apify Store right now."
- **0:25–0:55, while it runs.** "Under the hood we call Apify's Google Maps Reviews Scraper, which has 10,000 monthly users, so we don't build fragile scrapers. We score the reviews in code, so the number is explainable. Then Apify's OpenRouter Actor writes the brief, billed to Apify credit."
- **0:55–1:30, the output.** Show the Output tab: health score 68, trend declining. "The top issue is slow weekend service, flagged in 21% of reviews, with real quotes. Here are 3 actions for this week, and reply drafts ready to post to the 5 angry reviews nobody answered." Open the Markdown brief.
- **1:30–1:50, the money.** "$0.49 per outlet per brief, pay-per-event. Ravi's 6 outlets weekly cost about $12 a month. Agencies run it for all their clients on a schedule."
- **1:50–2:00, close.** "ReviewRx: a paragraph that replaces an hour of reading. Live on Apify Store." **Backup:** if the run hasn't finished by 0:55, switch to the pre-run tab of the identical run and say "same Actor, run 2 minutes ago."

---

## 8. Confidence: verified facts and assumptions

**Verified, from the pages listed above:**
- Store usage, rating and price figures.
- The PPE-only monetization model, the 20% cut and the 14-day notice rule with its no-paying-users exception.
- The publishing prerequisites and that there is no pre-publication review.
- That apify/openrouter exists, its endpoint and its 2,048-token cap.
- That the `.md` Store pages work.
- The agent-skills install commands as written in the README.

**Inferred or assumed:**
- A live run of 80 reviews finishes in under 60s. This is not timed; **measure it at 11:30**.
- The cost-per-brief estimate.
- The willingness-to-pay figures, which come by analogy to the SaaS reputation-tool category.
- The feeder Actor's exact input field names in the code sketch. Verify them on the `.md` page.
- Naukri's terms.

---

## 9. Open questions and assumptions

**Assumptions made**
- The team works in Python.
- One member's account owns and publishes the Actor, and the other members' credits are used for testing.
- Judges accept Google Maps review data obtained through an existing Store Actor as public data.
- Google Maps results for Bengaluru cafés are available at the venue.

**Information still needed, to check on the day**
1. **Who pays for child Actor runs?** When ReviewRx calls the reviews scraper, does the pay-per-event charge for that run land on the end user's account or on the developer's? This was not documented. Test it with a second account. If it lands on the developer, keep the $0.49 price, which already covers it.
2. **Does the $50 coupon credit count as a "paying" plan for OpenRouter?** Free-tier accounts pay 10x and may be blocked by anti-fraud checks. Make a test LLM call before 10:30. Fallback: a direct LLM API key stored as a secret environment variable (`apify secrets add`).
3. **The exact required Publishing-tab fields** (icon size, categories) were not documented. Check them at 11:45.
4. Confirm the OpenRouter model slug for the chosen model at build time.
5. Confirm with organisers that the team name "ReviewRx" (Actor `reviewrx`) is free, and that the direct-URL Store page is acceptable for judging.

---

## 10. Addendum: niche government open-data ideas (pharma and patents)

*Researched on 22 Nov 2026 at the team's request: build insight Actors on open government data instead of scraped consumer sites. The openFDA queries in this section were run live today.*

### 10.1 Data sources found

| Source | Status | Access | Verdict for today |
|---|---|---|---|
| **openFDA** (`api.fda.gov`) | **Tested live** | Free, works without a key. Without a key: 240 requests per minute and **1,000 per day per IP**. With a free key: 120,000 per day ([auth docs](https://open.fda.gov/apis/authentication/)). | **Best source.** One government JSON API covering the Orange Book, Drugs@FDA, recalls, shortages, labels and adverse events. |
| **openFDA Orange Book** (`/drug/orangebook.json`) | **Tested live** | 48,990 records, 2,701 of them with patents. Each record has `patents[].expiration_date`, `drug_substance_flag`, `drug_product_flag`, `patent_use_code`, `exclusivity[].exclusivity_code / _expiration_date`, `application_type` (N = brand, A = generic), `application_full_name`, `dosage_form`, `reference_listed_drug` and `therapeutic_equivalence_codes`. `last_updated` is 2026-11-20. | **The core dataset.** Count queries return in about 1 second. |
| FDA Orange Book zip (fda.gov) | Blocked | A curl request got a 404 even with a browser user-agent, which suggests bot blocking. | Use the openFDA copy instead. |
| openFDA `drug/enforcement` (recalls) | Tested by the research agent | Has a `country` field. `country:"India"` returned 301 recalls, rankable by `recalling_firm`. | Good secondary signal. The country is the *recalling* firm's. |
| openFDA `drug/shortages` | Endpoint confirmed by the agent | 1,581 records | A demand signal |
| ClinicalTrials.gov API v2 | Tested by the agent | No key needed. Filters by condition, phase and status. Returns sponsor and completion date. | Good for a pipeline-landscape idea |
| FDA warning letters | XLSX export only, no API, no country column, fda.gov may block servers | — | Avoid as a live dependency |
| FDA Data Dashboard API | Needs a key approved by email, turnaround unknown | — | Too risky today |
| CDSCO NSQ, NPPA, data.gov.in, CTRI (India) | The pages are built with JavaScript, block right-click and F12, return 403s, or are disallowed in robots.txt | — | **Avoid.** They're fragile and hostile to scraping. |
| **USPTO PatentsView API** | **Shut down.** Moved to the USPTO Open Data Portal on 20 Mar 2026 ([USPTO notice](https://www.uspto.gov/subscription-center/2026/patentsview-migrating-uspto-open-data-portal-march-20)). The Open Data Portal needs a USPTO.gov account since 18 Jun 2026 ([notice](https://www.uspto.gov/about-us/news-updates/uspto-open-data-portal-require-registration-access-beginning-june-18-2026)), and possibly an ID.me identity check (unverified). | — | Blocked for a same-day build |
| **EPO OPS** | Registration required. Free up to 4 GB a week ([EPO](https://www.epo.org/en/searching-for-patents/data/web-services/ops)). CQL search covers **title and abstract only, not claims**. Claims are fetched one patent at a time. | — | The only workable patent route. **Register first.** Whether signup is instant is unverified. |
| Google Patents | robots.txt blocks search pages. BigQuery public data is the sanctioned route, with 1 TB a month free, but needs a GCP service account. | — | Backup only |
| Lens.org, WIPO PATENTSCOPE | Lens access is reviewed by a person. WIPO's API is paid. | — | Not feasible today |

### 10.2 Store competition (figures from the Store API, 22 Nov 2026)
- **Pharma:** every Actor has 50 or fewer total users, and almost all return raw rows.
  - [nexgendata/fda-orange-book-drug-patents](https://apify.com/nexgendata/fda-orange-book-drug-patents): 0 monthly / 6 total users, raw.
  - [zentrafoundry/fda-orange-book-exclusivity-cliff-watcher](https://apify.com/zentrafoundry/fda-orange-book-exclusivity-cliff-watcher): 1 / 2 users, $0.002 per result, cliff dates only.
  - [taroyamada/fda-orange-book-patent-exclusivity-change-report](https://apify.com/taroyamada/fda-orange-book-patent-exclusivity-change-report): 1 / 2 users, **$18 per patent-cliff report**. This shows a creator pricing it as a premium report.
  - [benthepythondev/fda-recall-intelligence](https://apify.com/benthepythondev/fda-recall-intelligence): 0 / 11 users.
  - [parseforge/clinicaltrials-scraper](https://apify.com/parseforge/clinicaltrials-scraper): 2 / 50 users, raw.
  - **None combines patent cliffs, generic competition and demand into a filing decision.**
- **Patents:**
  - The leader is a raw scraper: `khadinakbar/google-patents-scraper`, 47 monthly users.
  - The closest idea-to-patents tool is [tacps126/innovation-radar](https://apify.com/tacps126/innovation-radar): 1 monthly user, $0.03 per analysis, EPO data, a crowding indicator, and no per-feature overlap or novelty score.
  - Demand on the Store is small.

### 10.3 Ranking

| Idea | Buyer | Buyer / Output / Shipped / Craft | Notes |
|---|---|---|---|
| **Patent Cliff Radar** (recommended) | US portfolio or BD head at an Indian generics company (the Sun, Lupin, Zydus, Aurobindo, Cipla type) | **5 / 5 / 5 / 5** | One keyless government API, about 1 s per query, and a clear India angle for Bengaluru judges. Pharma BD teams already pay for expensive intelligence subscriptions. |
| Indian Supplier FDA Risk Score | Procurement or QA at a US or EU buyer qualifying an Indian drug-ingredient supplier | 4 / 5 / 5 / 4 | Uses openFDA enforcement data only. Firm-name matching is fuzzy. **Good as a stretch section of the main idea.** |
| Prior-Art Novelty Brief | Startup founder, R&D manager, patent attorney doing a first screen | 4 / 5 / 3 / 4 | Depends on EPO registration, cannot search claims, and Store demand is small |
| Pharmacovigilance Signal Snapshot | PV team | 4 / 4 / 4 / 3 | The statistics need care to stay defensible |
| ReviewRx (section 5) | Ops head of a café chain | 4 / 5 / 5 / 5 | Still a solid fallback, but it uses a Google scraper |

### 10.4 Primary pick: Patent Cliff Radar

**Pitch:** which US drugs lose patent protection in your window, how crowded each generic market already is, and which 5 to file for first. One run instead of a week of an analyst's time in the Orange Book.

**Buyer:** "Head of US portfolio selection at a Hyderabad or Ahmedabad generics company." Indian firms file a large share of US generic applications. Choosing molecules 2–4 years ahead of patent expiry is their core recurring decision.

**Architecture** (Python, `python-start` template, `httpx` async, openFDA only, LLM through `apify/openrouter`):
1. **Candidates.** Find ingredients with a patent or exclusivity expiring in the window, ranked. Verified live today: for 2027–28 it returned METFORMIN HCL 43, OXYCODONE HCL 18, TREPROSTINIL 18, IVACAFTOR 17, EMPAGLIFLOZIN 16, and so on, in about 1 s.
   `GET /drug/orangebook.json?search=patents.expiration_date:[20270101+TO+20281231]&count=products.active_ingredients.name.exact&limit=100`
2. **Per candidate (top 30, run in parallel with concurrency 4):**
   - **Brand records** (`application_type:N`):
     - compute the **last blocking date** = max(latest patent expiry, latest exclusivity expiry) per brand application, and keep the candidate only if that date falls in the window
     - record the brand name, the holder, and the dosage forms
   - **Generic competition:**
     - `search=products.active_ingredients.name:"X"+AND+products.application_type:A&count=products.application_full_name.exact`
     - Verified for empagliflozin: ZYDUS PHARMACEUTICALS USA 6, INVAGEN 2.
     - Count the distinct approved generic holders.
     - Flag Indian firms with a hard-coded list of about 40 names and US subsidiaries: Zydus, Sun, Dr. Reddy's, Lupin, Aurobindo, Cipla/InvaGen, Glenmark, Torrent, Alkem/Ascend, Hetero/Camber, MSN, Natco, Macleods, Ajanta, Granules, Unichem, Alembic, Strides, Intas/Accord and others.
   - **Patent type:** if the remaining patents are **only method-of-use patents** (they have a `patent_use_code` and no `drug_substance_flag` or `drug_product_flag`), flag "carve-out possible: earlier entry via a section viii label". This is the insight that impresses domain experts.
   - **Demand signals:**
     - Is the ingredient on the current shortages list (`/drug/shortages.json`)?
     - FAERS report volume (`/drug/event.json?search=patient.drug.openfda.generic_name:"x"`, read `meta.results.total`), labelled clearly as a **usage proxy, not revenue**.
3. **Score from 0 to 100, computed in code:**
   - 35% timing: 18–36 months to the cliff is best for filing lead time
   - 30% competition gap: 0–2 generic holders is best, 10 or more is crowded
   - 20% demand proxy
   - 15% shortage, carve-out and complexity bonuses, such as injectables and harder dosage forms
4. **LLM step:**
   - A 2–3 sentence rationale per molecule.
   - A top-level memo, "File these 5 first, and why".
   - Instruct the model to use only the supplied numbers and never invent market sizes.
5. **Results:**
   - Push one row per molecule to the dataset.
   - Save `RADAR.md` to the key-value store.
   - Call `Actor.charge('molecule-scored')` once per row.

**Input schema:**

| Field | Type | Default |
|---|---|---|
| `windowStart` | string (`datepicker`) | today |
| `windowEnd` | string (`datepicker`) | today + 3 years |
| `dosageForms` | array (`select`, multiple): tablet, capsule, injectable, inhalation, topical, ophthalmic | all |
| `maxExistingGenerics` | integer | 5 |
| `myCompanyName` | string, optional | — (flags molecules where you already hold an approved generic) |
| `topN` | integer | 15 (max 40) |

**Sample output row (illustrative):**
```json
{
  "molecule": "EXAMPLE-INGREDIENT",
  "brand": "BRANDNAME", "brandHolder": "BRAND PHARMA INC",
  "dosageForms": ["TABLET"],
  "lastBlockingDate": "2028-03-14", "monthsToCliff": 28,
  "blockingType": "method-of-use only (carve-out possible)",
  "approvedGenericHolders": 1, "indianGenericHolders": ["ZYDUS PHARMACEUTICALS USA INC"],
  "inShortage": false, "faersReportVolume": 18234,
  "opportunityScore": 82,
  "verdict": "FILE NOW",
  "rationale": "28 months to the last blocking patent, which covers a method of use only, so a section viii carve-out could allow earlier entry. Only one approved generic holder…",
  "sources": ["https://api.fda.gov/drug/orangebook.json?search=…"]
}
```
Possible verdicts are `FILE NOW`, `WATCH` and `CROWDED - SKIP`. Every row carries its openFDA query URLs as evidence. This matters for trust, because openFDA's own disclaimer says results are "unvalidated".

**Pricing (pay-per-event):**
- **`molecule-scored`: $0.25.** A typical 20-molecule radar costs $5.
- **Cost per run:** about 60–90 openFDA calls (free), a few thousand LLM tokens and a small amount of compute. I estimate under $0.10 per run, so the margin is very high.
- **Positioning:** priced well below the $18-per-report Store comparable, and far below enterprise pharma-intelligence subscriptions. It stays cheap enough for a BD analyst to expense without a purchase order.
- **Optional stretch event:** `supplier-risk-check` at $0.50, the India recall score.

**Build timeline** (same structure as section 7):
- 10:15–10:30: get the openFDA key, scaffold, run the 3 test queries.
- 10:30–11:15: candidate and per-molecule fetch logic, plus the scoring.
- 11:15–11:45: LLM memo, schemas, then **`apify push` and the first cloud run**.
- 11:45–12:00: **publish**.
- 13:00–14:10: carve-out flag, Indian-firm list, README, `Actor.charge`. Stretch: the supplier risk section.
- 14:10–14:30: rehearse.

**Cut-scope order:**
1. Drop the FAERS demand proxy.
2. Drop shortages.
3. Drop the LLM memo and keep the deterministic verdicts and template sentences. It remains a decision tool.

**2-minute demo script:**
1. **Buyer, 0:00–0:15.** "Meet Priya, head of US portfolio at a Hyderabad generics company. Every quarter her team spends weeks in the FDA Orange Book deciding which molecules to file for."
2. **Live run, 0:15–0:25.** Open the Store page. Set the window to 2027–2029, oral solids, at most 5 existing generics. Click Start.
3. **While it runs, 0:25–0:50.** "This is 100% official FDA open data via openFDA. No scraping, no logins. We pull patent and exclusivity dates, count every approved generic competitor, flag Indian rivals, and check shortages. The score is computed in code, so it's explainable, and the LLM writes the memo."
4. **Output, 0:50–1:30.**
   - The top row reads FILE NOW, 82, with "remaining patent is method-of-use only, so a carve-out is possible".
   - Contrast it with an earlier search for empagliflozin, which has many patents expiring in 2027–28 but where "Zydus already holds 6 approved generics. Crowded, skip."
   - Open the `RADAR.md` memo.
5. **Money, 1:30–1:50.** "$0.25 per molecule scored. A 20-molecule radar costs $5, which replaces weeks of analyst time. Schedule it monthly and get alerts when the Orange Book changes."
6. **Close, 1:50–2:00.** "Patent Cliff Radar: a filing decision, not a database. Live on Apify Store."

**Risks and caveats:**
- **Rate limit.** The 1,000-per-day-per-IP limit without a key could be hit on shared Apify servers. **Get the free key first**, store it as a secret (`apify secrets add openfdaKey …`) and reference it in actor.json environment variables.
- **Missing data.** The Orange Book lists approved products only. It shows no tentative approvals, no pending Paragraph IV litigation and no market revenue, so state these limits in the README.
- **Name matching.** Matching Indian firms by name is a heuristic.
- **Terms.** openFDA's own terms and license are at [open.fda.gov/terms](https://open.fda.gov/terms/) and [open.fda.gov/license](https://open.fda.gov/license/). I didn't read them in full. Check them before publishing; it's a 2-minute read.
- **Window filter.** Filter candidates on the *last* blocking date. A raw count of patents expiring in the window includes drugs that still have later patents.

---

## 11. Will it get customers? Store demand by vertical

*Pulled live from `api.apify.com/v2/store` on 22 Nov 2026. "Monthly users (top 50)" is the sum of 30-day users across the top 50 search results.*

| Search term | Store results | Monthly users (top 50) | Top Actor's monthly users |
|---|---|---|---|
| google maps | 4,614 | **66,912** | 48,926 (compass/crawler-google-places) |
| linkedin jobs | 2,819 | **37,887** | 13,432 (curious_coder/linkedin-jobs-scraper) |
| google maps reviews | 2,288 | **11,213** | 10,005 (compass/Google-Maps-Reviews-Scraper) |
| leads | 50,895 | 10,312 | 1,774 |
| naukri | 236 | **6,393** | 2,891 (valig/naukri-jobs-scraper) |
| amazon reviews | 1,199 | 6,358 | 2,416 |
| trustpilot | 547 | 3,246 | 1,376 |
| g2 | 219 | 1,334 | 330 |
| funding / crunchbase | 9,088 / 257 | 894 / 875 | 180 |
| tender / government | 11,773 / 3,791 | 292 / 274 | 23 / 27 |
| indiamart / justdial / flipkart | 85 / 69 / 142 | 231 / 169 / 244 | 75 / 33 / 71 |
| patent | 5,858 | **119** | 47 |
| fda | 778 | **51** | 3 |
| pharma | 1,352 | **52** | 3 |
| clinical trials | 413 | **49** | 2 |

**What this means**
1. **People shopping on the Store aren't pharma or patent buyers.** Those categories have about 50–120 monthly users in total. A pharma business-development team buys intelligence through enterprise sales, not by searching Apify Store. Patent Cliff Radar has a real buyer but the wrong channel. It would only earn through direct outreach.
2. **Demand on the Store follows a data source people already search for:** Google Maps, LinkedIn/Naukri jobs, reviews, leads.
3. **Analysis-only Actors rarely gain traction on their own.** The 5+ Google-Maps lead scorers and review analyzers each have fewer than 10 monthly users. The Actors that pair analysis with traction are **scrapers for a popular source with AI insights bundled in**:
   - [memo23/g2-scraper](https://apify.com/memo23/g2-scraper), "Reviews… AI Insights + Emails": 208 monthly users, 4.3★ (7)
   - [memo23/apify-clutch-cheerio](https://apify.com/memo23/apify-clutch-cheerio), "+ AI Insights": 158 monthly users
   - [yumitori/etsy-search-scraper](https://apify.com/yumitori/etsy-search-scraper), "Quality Score & Product Analyzer": 245 monthly users
4. **Search visibility.** Since 19 Nov 2026, new low-usage Actors in crowded categories are hidden from Store search ([blog](https://blog.apify.com/apify-store-search-update/)). Pick a title that matches a *specific* search term (e.g. "Google Maps Reviews → AI Action Brief") rather than a generic one.

**Revised recommendation:** build where demand already exists, and make the conclusion the reason to choose you over the raw scraper.
- **ReviewRx** (section 5) is back to primary. It sits on 11,213 monthly users of review-scraper demand, the existing analyzers are stale, and it follows the proven "data + AI insights" pattern. Title it so it is found by search: "Google Maps Reviews Analyzer — AI Action Brief & Reply Drafts".
- **Alternative with an India angle: a Naukri hiring-intent brief.** Naukri scrapers have 6,393 monthly users, and no conclusion layer exists. Risk: Naukri's terms are unverified and likely forbid automated access.
- **Patent Cliff Radar:** pitch it only as "high value, sold direct". Expect judges, who earn from the Store, to ask about Store demand.
