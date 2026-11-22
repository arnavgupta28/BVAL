# BVAL: demo harness decision

How the 2-minute demo shows the two ways to use BVAL: a creator triggering it directly on Apify, and a creator's AI agent calling it as a tool. Decided 22 Nov 2026, revised the same day: the demo uses our own phone-styled pages in [demo/](demo/) for both paths, with the Store page shown as proof it's live on Apify.

| Path | Harness | What the viewer sees |
|---|---|---|
| **Direct, on Apify** | **"Check a deal" page** (`demo/`, `http://localhost:8787/`): fill the deal, it starts the live `agupta1/bval` Actor on Apify through the API, shows the run, then the report | The `QUOTE.html` deal report: verdict, price tiles, rate card (no-offer), "Your numbers", counter-offer email, price bar, red flags |
| Proof it's the real Store Actor | The public Store page (`apify.com/agupta1/bval`), one tab, 5 seconds | Same Actor, same form, the pay-per-event price |
| **Creator agent (LLM)** | **Agent chat page** (`demo/`, `http://localhost:8787/agent`): a **local LLM in LM Studio** (Qwen3.5-9B) with BVAL as its tool; Claude as a switchable fallback | Priya pastes the brand's DM; Claude turns it into BVAL input, calls BVAL, and answers with `nextAction`, the one-line `summary`, the report link and the designed counter-offer email |
| Backup for the agent | Claude (claude.ai) with the Apify MCP server, `https://mcp.apify.com/?tools=agupta1/bval` | Same flow inside Claude's own app, if the agent page fails |

Built by session apify-4e [fef7ec]: [demo/server.py](demo/server.py) plus the two pages. Tokens stay in the server; the pages never see them.

**Agent runs locally, tool runs on Apify.** The agent's model runs on this laptop in LM Studio (no API key, no per-message cost); every BVAL call it makes is still a live run of the Apify Actor, because BVAL is the Apify product and its scrapers only run there. That's the pitch: any agent, even a local one, can use BVAL.

## Why this choice

1. **It shows exactly the two stories.** "Here's the tool run directly on Apify" and "here's how a creator's AI agent uses it", side by side in the same visual style as the report.
2. **Both pages call the real, live Actor.** Nothing is mocked: the direct page starts an Apify run, and the agent's tool call is an Apify run. The Store tab proves it's the published Actor that judges can open.
3. **The agent turns a messy DM into structured input.** That's the value of the agent path: Priya doesn't fill a form, she pastes what the brand wrote. It shows why `nextAction` and `summary` exist.
4. **Local model, real tool.** Running the agent in LM Studio shows BVAL isn't tied to one AI provider, and keeps the demo free of API costs.
5. **A backup that needs no code.** Claude with the Apify MCP server is how any MCP agent would use BVAL, so it also backs up the claim in the README.

**Rejected:** n8n, Make or Zapier (automations, not agents); the API tab alone (proves nothing to a non-developer).

## Setup (do before the demo)

1. `apify push` (your OK) so the live Actor has no-offer mode, "Your numbers" and the designed counter-offer email. Today's live build 0.1.7 has the report and agent fields but not those three.
2. Publish BVAL on the Store (see [apify_console_config.md](apify_console_config.md)).
3. Start the demo server with the two secrets in the environment, never in a file you commit:
   `APIFY_TOKEN=… LM_API_TOKEN=… demo/.venv/bin/python demo/server.py`, then open `http://localhost:8787` and `/agent`. In LM Studio, load **Qwen3.5-9B-MLX-4bit** first (the 1.7B and 2B models are too small for reliable tool calls). Add `ANTHROPIC_API_KEY` only if you want the Claude fallback.
4. Dry-run the agent prompt below once. Check that the agent fills `offer.amount`, `rights.organicUsageDays`, `rights.whitelistingDays`, `rights.exclusivityDays` and `niche: fitness` from the DM.
5. Backup: in claude.ai → Settings → Connectors → **Add custom connector** with `https://mcp.apify.com/?tools=agupta1/bval`.

**Agent prompt for the demo:**
> Acme Protein just DM'd me: "We'd love $800 for one Reel, plus 90 days to reuse it, 30 days running it as a Partnership Ad, and 6 months fitness exclusivity." I'm @&lt;demo handle&gt; on Instagram. Should I take it?

Use the same handle on both pages so both paths give the same verdict. The prices below ($2,790 fair, $910 walk-away) come from the manual-metrics demo input (85k followers, 42k median views). A scraped handle gives different numbers, so rewrite those lines after the backup run.

## 2-minute script

Each run takes about 60s, so start both runs early and talk while they run.

| Time | Screen | Line |
|---|---|---|
| 0:00–0:12 | Brand DM | "Priya got $800 for a Reel, 90 days usage, 30 days of ads and 6 months exclusivity. Fair?" |
| 0:12–0:22 | **"Check a deal" page** → Start | "Run it directly: this starts BVAL live on Apify." |
| 0:22–0:32 | **Agent page** → paste the DM, send | "Or her AI agent does it, here a local model on this laptop. She just pastes the DM." |
| 0:32–0:50 | Run progress; Store tab for 5 seconds | "It's the published Store Actor. Apify's scrapers get her real median views; a cited pricing engine does the maths; the LLM only writes the email." |
| 0:50–1:20 | **Deal report** | "Fair is $2,790; $800 is below her walk-away. Here's why: 42,000 views at $20 per thousand, engagement in range, fitness pays more. Exclusivity alone is worth $1,360. Two options and the email, ready to send." |
| 1:20–1:42 | **Agent's answer** | "Her agent got the same verdict as one line it can act on, a link to the same report, and the counter-offer as a designed email to forward." |
| 1:42–1:52 | Report of a no-offer run (pre-run) | "No offer yet? BVAL tells her what to pitch: Starter, Standard, Premium." |
| 1:52–2:00 | Store page price | "$0.99 a deal, pay-per-event. BVAL: know your worth before you reply." |

**Fallbacks:** keep a finished run on each page and a finished no-offer report open in tabs. If a live call is slow, cut to the finished one. If the agent page fails, use the claude.ai MCP backup.

## To verify before the demo

- Both pages run against the pushed build (check the report shows "Your numbers" and, for no-offer, the packages).
- The agent page's tool call waits for a ~60s run and returns the dataset row.
- Qwen3.5-9B turns the DM into the right input (amount 800, 90/30/180 days, niche fitness) in 3 of 3 dry runs. If it doesn't, switch the agent page to the Claude fallback.
- The local model's first reply after loading is slow: send one warm-up message before recording.
- `reportUrl` and `counterEmailUrl` open without logging in (signed links; checked for `reportUrl` on build 0.1.7).
- Charging: runs on your own Actor aren't billed to you, so demo runs only cost the scrapers.
