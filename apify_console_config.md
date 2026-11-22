# BVAL: Apify Console configuration

Exactly what to enter in Apify Console to publish BVAL on Apify Store, and why each value was chosen. Work top to bottom: each section unblocks the next.

| | |
|---|---|
| Actor | `agupta1/bval`, build 0.1.4, [Console](https://console.apify.com/actors/pvlXeWRnGfAg9NI0j) |
| Status today | Private, limited permissions, 3 runs, latest cloud run succeeded in 56s |
| Credit | $0.69 used of $55 |
| Order | 1 Public profile → 2 Display information → 3 Monetization → 4 Permissions and schemas → 5 Publish → 6 Verify |

---

## 1. Public profile (blocker)

Console shows *"You need a public account to publish Actors."* Nothing below can be published until this is done.

**Where:** Publishing tab → **Set up public profile** (or Settings → Account → Public profile).

| Field | Value |
|---|---|
| Username | `agupta1` (keep it: it is already in the Actor ID `agupta1/bval` and in every API and run link) |
| Display name | Arnav Gupta |
| Bio (optional) | Builder of BVAL, a brand-deal valuation tool for creators. |
| Avatar (optional) | Any photo, or reuse the BVAL logo |

**Why:**
- Store pages show the author. Apify requires a public identity so buyers know who maintains a paid tool.
- Changing the username now would change the Actor's URL. The judges' link, the README and the API examples all assume `agupta1/bval`.

---

## 2. Display information

**Where:** Publishing tab → **Display information**.

| Field | Value | Reasoning |
|---|---|---|
| Actor icon | `logo/bval-logo-512.png` | The API rejects outside image links, so the icon must be uploaded here. 512×512 stays sharp at every Store size. |
| Title | `BVAL: Brand Deal Rate Calculator for Creators` | Leads with the brand (the team name must match "BVAL"), then the search phrase creators type: "brand deal rate calculator". |
| Short description | `Paste a brand offer, get the verdict: fair rate, itemised usage, whitelisting and exclusivity, walk-away/floor/ask, and a counter-offer email. Instagram, TikTok, YouTube.` | Already in `actor.json`. It states the input, the output and the platforms in one line, and shows the *output is a decision*, which is the hackathon's "Output" criterion. |
| Categories | **AI**, **Social media**, **Marketing** (or **Business** if Marketing is not offered) | AI because the email is LLM-written and the Actor is agent-callable; Social media because the inputs are Instagram/TikTok/YouTube handles; Marketing or Business because the buyers are creators, managers and agencies. Avoid "Lead generation": it attracts the wrong searchers. |
| SEO title (≤ 60 chars) | `Influencer Rate Calculator: Brand Deal Pricing API \| BVAL` | Targets "influencer rate calculator", the highest-volume phrase, plus "API" for developers and agents. |
| SEO description (≤ 160 chars) | `Price any creator brand deal from real views: usage rights, Partnership & Spark Ads, exclusivity. Get a verdict and counter-offer email. IG, TikTok, YouTube.` | Fits Google's snippet length; names the three things competitors don't itemise. |
| README | Already deployed from `bval/README.md` | No action. Check it renders (section 6). |

---

## 3. Monetization: pay-per-event

**Where:** Publishing tab → **Monetization → Set up monetization**. The form has three steps: *Actor pricing → Primary event → Review*.

### 3.0 Cost and profit per request (measured 22 Nov 2026)

Costs come from real runs on this account (Apify run usage). Revenue is what the user pays; Apify keeps 20%, so we net 80%.

| Request | User pays | We net (80%) | Our cost, Sonnet 4.5 | Our cost, Sonnet 5.5 | Profit (5.5) | Margin on net (5.5) |
|---|---|---|---|---|---|---|
| Instagram deal + email | $0.99 | $0.792 | $0.178 | $0.223 | **$0.57** | 72% |
| TikTok deal + email | $0.99 | $0.792 | $0.185 | $0.230 | **$0.56** | 71% |
| YouTube deal + email | $0.99 | $0.792 | $0.255 | $0.300 | **$0.49** | 62% |
| Instagram deal, no email | $0.79 | $0.632 | $0.095 | $0.095 | **$0.54** | 85% |
| Re-price (own numbers) + email | $0.45 | $0.360 | $0.085 | $0.130 | **$0.23** | 64% |
| Re-price, no email | $0.25 | $0.200 | $0.002 | $0.002 | **$0.20** | 99% |

Cost parts: Instagram scrapers $0.079 + $0.0026, TikTok scraper $0.09, YouTube scraper $0.16, BVAL compute $0.012-0.014 scraped / ~$0.002 manual, email via Apify's AI proxy $0.083 (Sonnet 4.5, stable) or $0.128 (Sonnet 5.5, one run), "email me the result" $0.0005 (negligible). The Actor-start fee ($0.00005) is ignored.

**This is the worst case**: it assumes we pay for the scrapers and the AI proxy. Those child runs start under the user's own token, so they may land on the user's bill instead; then our cost is only BVAL's compute (~$0.002-0.014) and the margin is ~98%. Confirm with one run from a second account (Open questions).

**Thinnest spot:** the email event on its own. With Sonnet 5.5 it costs ~$0.13 and nets $0.16 (+$0.03). It's fine as part of a $0.99 deal check; if most buyers re-price with emails, raise `counter-email-drafted` to $0.29.

**At volume** (Sonnet 5.5, Instagram + email): 100 deal checks a month ≈ $57 profit; 1,000 ≈ $570.

### 3.1 Events

Your form starts with two default events plus an empty one. Final setup:

| Event name (exact) | Title | Price | Action | Infrequent? |
|---|---|---|---|---|
| `apify-actor-start` | Actor Start | **$0.00005** (default) | **Keep** | No |
| `apify-default-dataset-item` | result | $0.00001 | **Remove** | n/a |
| `deal-evaluated` | Deal evaluated | **$0.79** | **Add** (replace `some-event`) | No |
| `counter-email-drafted` | Counter-offer email drafted | **$0.20** | **Add** | No |
| `manual-deal-evaluated` | Deal re-priced (manual metrics) | **$0.25** | **Add** | Yes |

The event names must match the code character for character. `main.py` calls `Actor.charge(event_name='deal-evaluated')` and so on, and a name that doesn't match is never billed.

**Descriptions to paste:**
- `deal-evaluated`: *Charged once per run after the creator is scraped and the deal is fully priced: line items, walk-away/floor/fair/ask range, verdict and red flags.*
- `counter-email-drafted`: *Charged when a ready-to-send counter-offer email is generated (generateEmail = true).*
- `manual-deal-evaluated`: *Charged instead of "Deal evaluated" when you supply manual metrics, so no scraping happens. Use it to re-price new terms.*

**Why these events and prices:**

1. **Charge for the decision, not the rows.** BVAL writes one dataset row per deal. Its value is the verdict and the email, not the row count, so per-row billing means nothing to the buyer. That's why the default `apify-default-dataset-item` event goes. Keeping it would also charge for error rows, since a failed creator lookup still writes one row explaining the error.
2. **$0.79 per deal evaluated.**
   - **Costs:** the scrapers cost us about $0.08 (Instagram), $0.09 (TikTok) and $0.16 (YouTube) per creator in today's test runs, plus about $0.01 of compute. Console's "average usage cost per 1,000 results is $12.11" is about $0.012 per run.
   - **Margin:** Apify keeps 20%, so we net $0.63 per evaluation, roughly 4-8x cost on Instagram and TikTok and about 4x on YouTube.
   - **Competition:** the closest Store competitor (`hypebridge/hypebridge-pricing`) charges about $1.95 per handle and gives no verdict or email.
3. **$0.20 for the email, as a separate event.** Users who only want numbers (agencies feeding their own CRM) can turn the email off and pay $0.79. Everyone else pays $0.99 for the full deal check. The LLM call costs about $0.01-0.03, so this event is almost all margin, and it's the feature competitors lack.
4. **$0.25 for manual re-pricing.** With no scrape, our cost is near zero. Creators often re-run a deal with different terms ("what if exclusivity is 30 days?"). A cheap re-price encourages that habit. It's marked *infrequent* because most runs scrape.
5. **Keep `apify-actor-start` at the default $0.00005.** It's negligible to the user. Per Console, defining it waives the first 5 seconds of run cost, which covers BVAL's startup.

### 3.2 Infrequent event toggle

Mark only `manual-deal-evaluated` as infrequent. The Store's headline price is built from the events most runs trigger. Marking the re-price event infrequent keeps the displayed price at "$0.79 per deal + $0.20 per email", which is what most users pay. *(Check the toggle's tooltip in Console; if it means something else, leave every event unmarked.)*

### 3.3 Store pricing discounts / cheaper unit pricing

**Leave off for now.** Tiered discounts by plan matter once volume buyers exist. During the hackathon, one clear price reads better in the demo ("$0.99 a deal"). Revisit if agencies start running hundreds of deals a month.

### 3.4 Additional options

| Option | Setting | Reasoning |
|---|---|---|
| **Pay per event + usage** | **OFF** | With it on, users also pay platform usage on top, which makes the cost unpredictable and the pitch muddier. The research also found the switch takes about **14 days** to take effect, so it would not apply before judging. Our event prices already cover our costs. |
| **Minimum for max cost per run** | **$1.00** | Users can cap a run's spend. If someone caps at $0.10, BVAL would still pay for the scrapers but could never charge the $0.79, a pure loss. A $1.00 minimum ensures the cap always covers a full deal ($0.79 + $0.20 + start fee ≈ $0.99). |

### 3.5 Primary event

Choose **`deal-evaluated`**. It's the event every scraped run triggers, and it's the unit the README, the demo and the competitor comparison all use ("per deal").

### 3.6 Review

Before confirming, check:
- 4 events listed: actor-start, deal-evaluated, counter-email-drafted, manual-deal-evaluated
- No `apify-default-dataset-item`
- "Pay per event + usage" is off
- Minimum max cost is $1.00

The new price applies straight away, because the Actor has no paying users yet. Apify's 14-day price-change notice only protects existing users.

---

## 4. Permissions, input schema and output schema

| Section | Setting | Reasoning |
|---|---|---|
| **Actor permissions** | **Limited** (already set) | Limited is enough. Today's cloud run called the Instagram scrapers successfully under "LIMITED_PERMISSIONS". Full permissions would trigger identity verification and slow publishing for no benefit. |
| **Input schema** | No change (deployed) | 30+ fields in sections (offer, usage/ads/exclusivity, production, contract, market/email, advanced). The form is prefilled with the demo deal, so a judge can click Start straight away. |
| **Output schema** | No change (deployed) | Three outputs: the "Deal verdict" table view, the `QUOTE.md` Markdown report, and the full JSON. The output schema is required for publishing. |

---

## 5. Publish on Store

**Where:** Publishing tab → **Publish on Store**.

Required, and already done:
- ✅ At least one successful run
- ✅ README
- ✅ Input and output schemas
- ✅ Limited permissions

You need to do:
- 🟡 Public profile (section 1)
- 🟡 Display information including the icon (section 2)
- 🟡 Monetization (section 3)

After publishing, **copy the direct Store URL** (`https://apify.com/agupta1/bval`). New, low-usage Actors can be hidden from Store search, so judges need the direct link.

---

## 6. Verify after publishing

1. Open the Store URL while logged out (private window) and check:
   - the icon, title and README render
   - the price shows "$0.79 / deal evaluated"
2. Run it from the Store page, logged in, once per platform:
   - Instagram `humansofny`
   - TikTok `khaby.lame`
   - YouTube `mkbhd`, with `youtube_integration`
3. In each run, confirm:
   - **Charged events** shows `deal-evaluated: 1` and `counter-email-drafted: 1`. If not, an event name doesn't match the code.
   - the **Output** tab shows the "Deal verdict" table and `QUOTE.md`
   - the run time is under about 60s
4. Keep one successful run open in a tab as the **demo backup**.

---

## Open questions

- **Who pays for the scraper runs BVAL starts?** Apify's docs don't say. If a user's run is billed to the user's account, our margin rises to nearly 100%; if it's billed to us, the margins above hold. Check it with a run from a second account and compare both accounts' usage.
- **Honouring the user's spending cap in code.** Right now BVAL charges after the work is done. A follow-up should check the run's remaining budget *before* scraping and stop early if `deal-evaluated` can't be charged. The $1.00 minimum (3.4) covers this for now.
