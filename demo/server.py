"""Local demo server for BVAL: a "Check a deal" page and a creator-agent chat page, both phone-styled.

  /         run page: fill the deal, start the live BVAL Actor on Apify, watch it run, open the report
  /agent    agent page: paste a brand's DM; an AI agent turns it into BVAL input, calls BVAL, answers

The agent's model runs locally in LM Studio by default (AGENT_BACKEND=lmstudio); set AGENT_BACKEND=claude to use
Claude instead. Either way, every tool call is a live run of the BVAL Actor on Apify.

Secrets stay here, never in the pages or the logs:
  APIFY_TOKEN        Apify Console > Settings > API & Integrations
  LM_API_TOKEN       LM Studio > Developer > server settings (the local server requires it)
  ANTHROPIC_API_KEY  only for AGENT_BACKEND=claude

Optional: LMSTUDIO_URL (default http://127.0.0.1:1234/v1), LMSTUDIO_MODEL (default qwen/qwen3.5-9b)

Run:  APIFY_TOKEN=... LM_API_TOKEN=... demo/.venv/bin/python demo/server.py   then open http://localhost:8787
"""

from __future__ import annotations

import json
import os
import queue
import re
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import anthropic
import openai
from apify_client import ApifyClient

ACTOR_ID = os.environ.get('BVAL_ACTOR', 'agupta1/bval')
PORT = int(os.environ.get('PORT', '8787'))
MODEL = 'claude-opus-5-5'
AGENT_BACKEND = os.environ.get('AGENT_BACKEND', 'lmstudio').lower()
LMSTUDIO_URL = os.environ.get('LMSTUDIO_URL', 'http://127.0.0.1:1234/v1')
LMSTUDIO_MODEL = os.environ.get('LMSTUDIO_MODEL', 'qwen/qwen3.5-9b')
STATIC = Path(__file__).resolve().parent / 'static'
FINAL = {'SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT', 'TIMED_OUT'}

_apify: ApifyClient | None = None
_claude: anthropic.Anthropic | None = None
_local: openai.OpenAI | None = None
_conversations: dict[str, list[dict[str, Any]]] = {}
_lock = threading.Lock()


def apify() -> ApifyClient:
    global _apify
    if _apify is None:
        token = os.environ.get('APIFY_TOKEN')
        if not token:
            raise RuntimeError('APIFY_TOKEN is not set. Export it before starting the server.')
        _apify = ApifyClient(token)
    return _apify


def local_llm() -> openai.OpenAI:
    """LM Studio's OpenAI-compatible server. Its API token comes from the environment, never from the page."""
    global _local
    if _local is None:
        token = os.environ.get('LM_API_TOKEN')
        if not token:
            raise RuntimeError('LM_API_TOKEN is not set. Copy it from LM Studio and export it before starting the server.')
        _local = openai.OpenAI(base_url=LMSTUDIO_URL, api_key=token, timeout=180)
    return _local


def claude() -> anthropic.Anthropic:
    global _claude
    if _claude is None:
        _claude = anthropic.Anthropic()
    return _claude


# ------------------------------------------------------------------------------------------------
# BVAL runs
# ------------------------------------------------------------------------------------------------

def start_run(run_input: dict) -> str:
    run = apify().actor(ACTOR_ID).start(run_input=run_input)
    return run.id


def run_state(run_id: str) -> dict:
    run = apify().run(run_id).get()
    if run is None:
        return {'status': 'UNKNOWN'}
    status = getattr(run.status, 'value', str(run.status))
    state: dict[str, Any] = {'status': status, 'message': run.status_message or ''}
    if status == 'SUCCEEDED':
        items = apify().dataset(run.default_dataset_id).list_items(limit=1).items
        state['item'] = items[0] if items else None
    return state


def wait_for_run(run_id: str, on_progress, timeout_s: int = 240) -> dict:
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        state = run_state(run_id)
        msg = state.get('message') or state['status']
        if msg != last:
            on_progress(msg)
            last = msg
        if state['status'] in FINAL:
            return state
        time.sleep(3)
    return {'status': 'TIMED-OUT', 'message': 'The run took longer than expected.'}


def report_html(run_id: str, key: str = 'QUOTE.html') -> str | None:
    run = apify().run(run_id).get()
    if run is None:
        return None
    record = apify().key_value_store(run.default_key_value_store_id).get_record(key)
    if not record:
        return None
    value = record.get('value')
    return value.decode() if isinstance(value, bytes) else value


# ------------------------------------------------------------------------------------------------
# Creator agent: Claude reads the DM, fills BVAL's input, calls it, and answers in plain words
# ------------------------------------------------------------------------------------------------

SYSTEM = """You are the AI assistant of a social media creator. Brands send them partnership offers by DM \
or email, and you help them answer.

When the creator shares a brand offer, call check_brand_deal to get a fair-value verdict before you give any \
opinion on price. Fill the tool input from what the brand actually wrote: the fee, each deliverable, and every \
usage, ads (Partnership Ads / Spark Ads / whitelisting), and exclusivity term with its duration in days \
(1 month = 30, 6 months = 180). Set niche from the brand or the content (a protein brand or "fitness exclusivity" \
means fitness). If the brand has not named a fee, or the creator wants to pitch first, set noOffer to true and \
leave offerAmount out. Leave out anything the brand did not mention. If the creator's handle or platform is \
missing, ask for it in one short question instead of guessing.

After the tool answers, reply like a sharp talent manager texting the creator:
- First line: the decision and the number to send (for example "Counter at $3,490.").
- Then two or three short lines on why, using the tool's prices and red flags. Never invent a number.
- Then the two options to offer if the tool gives a reduced scope, or the ready-made packages if it gives a rate card.
- End with "Full report: <reportUrl>" and, when the tool returns counterEmailUrl, "Counter email: <counterEmailUrl>".
Keep it under 120 words, no headings, no tables. Do not paste the counter-offer email text; the link opens it."""

DELIVERABLES = ['instagram_reel', 'instagram_story_frame', 'instagram_static_post', 'instagram_carousel',
                'tiktok_video', 'youtube_integration', 'youtube_mention_15_30s', 'youtube_dedicated', 'youtube_short']
NICHES = ['lifestyle', 'finance', 'business_saas', 'tech', 'education', 'health', 'health_credentialed', 'fitness',
          'beauty', 'fashion', 'travel', 'food', 'parenting', 'entertainment', 'gaming', 'other']

TOOL = {
    'name': 'check_brand_deal',
    'description': ("Values a brand partnership offer for a creator with BVAL. Reads the creator's real recent views, "
                    'prices every term of the deal from cited 2026 benchmarks, and returns a verdict (accept, counter, '
                    'decline, or quote), the walk-away / floor / fair / ask prices, red flags, a reduced-scope option, '
                    'and a link to the full report. Takes about a minute.'),
    'strict': True,
    'input_schema': {
        'type': 'object',
        'additionalProperties': False,
        'required': ['platform', 'handle'],
        'properties': {
            'platform': {'type': 'string', 'enum': ['instagram', 'tiktok', 'youtube']},
            'handle': {'type': 'string', 'description': 'Creator handle without @, or profile URL.'},
            'niche': {'type': 'string', 'enum': NICHES},
            'brandName': {'type': 'string'},
            'offerAmount': {'type': 'integer', 'description': 'Total fee offered for the whole deal.'},
            'noOffer': {'type': 'boolean', 'description': 'True when the brand has not named a fee yet: BVAL then suggests what to charge.'},
            'currency': {'type': 'string', 'enum': ['USD', 'INR', 'GBP', 'EUR', 'BRL', 'MXN', 'CAD', 'AUD', 'IDR', 'JPY', 'PHP']},
            'deliverables': {
                'type': 'array',
                'items': {
                    'type': 'object', 'additionalProperties': False, 'required': ['type', 'qty'],
                    'properties': {'type': {'type': 'string', 'enum': DELIVERABLES}, 'qty': {'type': 'integer'}},
                },
            },
            'organicUsageDays': {'type': 'integer', 'description': 'Days the brand may repost the content organically.'},
            'paidUsageDays': {'type': 'integer', 'description': "Days the brand may run the content as ads from its own account."},
            'whitelistingDays': {'type': 'integer', 'description': "Days of Partnership Ads / Spark Ads run through the creator's handle."},
            'exclusivityDays': {'type': 'integer', 'description': 'Days the creator may not work with competing brands.'},
        },
    },
}

# Demo creators the agent can price without scraping (fast, no scraper cost). Any other handle is scraped live.
DEMO_METRICS = {
    'priya.fit': {'followers': 85000, 'medianViews': 42000, 'engagementRate': 0.035},
}


def tool_input_to_bval(t: dict) -> dict:
    run: dict[str, Any] = {'platform': t['platform'], 'handle': t['handle'].lstrip('@'), 'generateEmail': True}
    if t.get('niche'):
        run['niche'] = t['niche']
    offer = {k: v for k, v in (('brandName', t.get('brandName')), ('amount', t.get('offerAmount')),
                               ('currency', t.get('currency'))) if v is not None}
    if t.get('noOffer'):
        offer = {k: v for k, v in offer.items() if k != 'amount'} | {'noOffer': True}
    if offer:
        run['offer'] = offer
    if t.get('deliverables'):
        run['deliverables'] = t['deliverables']
    rights = {k: t[k] for k in ('organicUsageDays', 'paidUsageDays', 'whitelistingDays', 'exclusivityDays') if t.get(k)}
    if rights:
        run['rights'] = rights
    metrics = DEMO_METRICS.get(run['handle'].lower())
    if metrics:
        run['manualMetrics'] = metrics
    return run


def tool_result_for_agent(item: dict) -> dict:
    """The fields the agent needs, kept small so a local model's context isn't flooded."""
    keep = ('nextAction', 'summary', 'reportUrl', 'counterEmailUrl', 'verdict', 'offerDisplay', 'priceRange', 'gapPct',
            'counterOptions', 'redFlags', 'confidence')
    out = {k: item[k] for k in keep if k in item}
    out['lineItems'] = [{'item': li['item'], 'amount': li['amount']} for li in item.get('lineItems') or []]
    if item.get('rateCard'):
        out['packages'] = [{k: p[k] for k in ('name', 'ask', 'fair', 'includes')} for p in item['rateCard'].get('packages') or []]
    return out


def run_bval_tool(tool_input: dict, emit) -> tuple[bool, str]:
    """Run BVAL on Apify for one tool call. Returns (ok, content for the model). Shared by both agent backends."""
    run_input = tool_input_to_bval(tool_input)
    emit('tool_call', {'input': run_input})
    try:
        run_id = start_run(run_input)
        emit('progress', {'message': 'BVAL run started', 'runId': run_id})
        state = wait_for_run(run_id, lambda m: emit('progress', {'message': m, 'runId': run_id}))
    except Exception as e:  # noqa: BLE001 - any Apify failure goes back to the model as a tool error
        emit('progress', {'message': 'BVAL could not run'})
        return False, f'BVAL could not run: {e}'
    item = state.get('item')
    if state['status'] != 'SUCCEEDED' or not item or item.get('error'):
        reason = (item or {}).get('error') or state.get('message') or state['status']
        emit('progress', {'message': f'BVAL: {reason}'})
        return False, f'BVAL run did not finish: {reason}'
    emit('tool_done', {'runId': run_id, 'item': item})
    return True, json.dumps(tool_result_for_agent(item))


THINK = re.compile(r'<think>.*?</think>\s*', re.S)


def agent_turn_local(convo_id: str, user_text: str, emit) -> None:
    """Agent loop on a local model in LM Studio (OpenAI-compatible tools API)."""
    tools = [{'type': 'function', 'function': {'name': TOOL['name'], 'description': TOOL['description'],
                                               'parameters': TOOL['input_schema']}}]
    with _lock:
        messages = _conversations.setdefault(convo_id, [{'role': 'system', 'content': SYSTEM}])
        messages.append({'role': 'user', 'content': user_text})
    for _ in range(4):
        try:
            response = local_llm().chat.completions.create(
                model=LMSTUDIO_MODEL, messages=messages, tools=tools, temperature=0.2, max_tokens=2048)
        except RuntimeError as e:
            emit('error', {'message': str(e)})
            return
        except openai.AuthenticationError:
            emit('error', {'message': 'LM Studio rejected the API token. Check LM_API_TOKEN on the demo server.'})
            return
        except openai.APIConnectionError:
            emit('error', {'message': f'Could not reach LM Studio at {LMSTUDIO_URL}. Is its server running with the model loaded?'})
            return
        except openai.APIStatusError as e:
            emit('error', {'message': f'LM Studio error ({e.status_code}).'})
            return
        msg = response.choices[0].message
        text = THINK.sub('', msg.content or '').strip()
        calls = msg.tool_calls or []
        entry: dict[str, Any] = {'role': 'assistant', 'content': text}
        if calls:
            entry['tool_calls'] = [{'id': c.id, 'type': 'function', 'function': {'name': c.function.name, 'arguments': c.function.arguments}}
                                   for c in calls]
        messages.append(entry)
        if text:
            emit('text', {'text': text})
        if not calls:
            emit('done', {})
            return
        for c in calls:
            try:
                args = json.loads(c.function.arguments or '{}')
                if not args.get('platform') or not args.get('handle'):
                    raise ValueError('platform and handle are required')
            except (json.JSONDecodeError, ValueError) as e:
                messages.append({'role': 'tool', 'tool_call_id': c.id, 'content': f'Invalid tool input ({e}). Fix it and call the tool again.'})
                continue
            _, content = run_bval_tool(args, emit)
            messages.append({'role': 'tool', 'tool_call_id': c.id, 'content': content})
    emit('done', {})


def agent_turn(convo_id: str, user_text: str, emit) -> None:
    """One user turn of the agent. Emits UI events: text, tool_call, progress, tool_done, error, done."""
    if AGENT_BACKEND != 'claude':
        return agent_turn_local(convo_id, user_text, emit)
    return agent_turn_claude(convo_id, user_text, emit)


def agent_turn_claude(convo_id: str, user_text: str, emit) -> None:
    """Agent loop on Claude."""
    with _lock:
        messages = _conversations.setdefault(convo_id, [])
        messages.append({'role': 'user', 'content': user_text})
    for _ in range(4):  # one tool call per turn is normal; the cap stops a runaway loop
        try:
            response = claude().beta.messages.create(
                model=MODEL,
                max_tokens=16000,
                system=SYSTEM,
                tools=[TOOL],
                messages=messages,
                output_config={'effort': 'low'},
                betas=['server-side-fallback-2026-07-01'],
                fallbacks='default',
            )
        except anthropic.AuthenticationError:
            emit('error', {'message': 'The Anthropic API key is missing or invalid on the demo server.'})
            return
        except anthropic.RateLimitError:
            emit('error', {'message': 'Claude is rate-limited right now. Try again in a minute.'})
            return
        except anthropic.APIStatusError as e:
            emit('error', {'message': f'Claude API error ({e.status_code}).'})
            return
        except anthropic.APIConnectionError:
            emit('error', {'message': 'Could not reach the Claude API. Check the network.'})
            return

        if response.stop_reason == 'refusal':
            emit('error', {'message': 'The assistant declined this request.'})
            return
        messages.append({'role': 'assistant', 'content': response.content})
        for block in response.content:
            if block.type == 'text' and block.text.strip():
                emit('text', {'text': block.text})
        if response.stop_reason != 'tool_use':
            emit('done', {})
            return

        results = []
        for block in response.content:
            if block.type != 'tool_use':
                continue
            ok, content = run_bval_tool(block.input, emit)
            result = {'type': 'tool_result', 'tool_use_id': block.id, 'content': content}
            if not ok:
                result['is_error'] = True
            results.append(result)
        messages.append({'role': 'user', 'content': results})
    emit('done', {})


# ------------------------------------------------------------------------------------------------
# HTTP
# ------------------------------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = 'BVALDemo/1.0'

    def log_message(self, fmt, *args):  # quieter log, and never the request bodies
        print(f'{self.address_string()} {fmt % args}')

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data: Any, code: int = 200) -> None:
        self._send(code, json.dumps(data).encode(), 'application/json')

    def _body(self) -> dict:
        n = int(self.headers.get('Content-Length') or 0)
        return json.loads(self.rfile.read(n) or b'{}')

    def do_GET(self):  # noqa: N802
        path = self.path.split('?')[0]
        pages = {'/': 'run.html', '/agent': 'agent.html'}
        if path in pages or path.startswith('/static/'):
            name = pages.get(path) or path.removeprefix('/static/')
            file = (STATIC / name).resolve()
            if not file.is_relative_to(STATIC) or not file.is_file():
                return self._send(404, b'Not found', 'text/plain')
            ctype = {'.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript'}.get(file.suffix, 'application/octet-stream')
            return self._send(200, file.read_bytes(), ctype)
        if path.startswith('/api/run/'):
            try:
                return self._json(run_state(path.rsplit('/', 1)[1]))
            except Exception as e:  # noqa: BLE001
                return self._json({'status': 'ERROR', 'message': str(e)}, 502)
        if path.startswith('/report/'):
            parts = path.split('/')
            key = 'COUNTER_EMAIL.html' if len(parts) > 3 and parts[3] == 'email' else 'QUOTE.html'
            try:
                html = report_html(parts[2], key)
            except Exception as e:  # noqa: BLE001
                return self._send(502, f'Could not load the report: {e}'.encode(), 'text/plain')
            if not html:
                return self._send(404, b'Report not ready', 'text/plain')
            return self._send(200, html.encode(), 'text/html; charset=utf-8')
        return self._send(404, b'Not found', 'text/plain')

    def do_POST(self):  # noqa: N802
        if self.path == '/api/run':
            try:
                return self._json({'runId': start_run(self._body())})
            except Exception as e:  # noqa: BLE001
                return self._json({'error': str(e)}, 502)
        if self.path == '/api/agent':
            body = self._body()
            convo_id = body.get('conversation') or uuid.uuid4().hex
            text = (body.get('text') or '').strip()
            if not text:
                return self._json({'error': 'Empty message'}, 400)
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            events: queue.Queue = queue.Queue()

            def emit(kind: str, data: dict) -> None:
                events.put((kind, data))

            emit('conversation', {'id': convo_id})
            worker = threading.Thread(target=lambda: (agent_turn(convo_id, text, emit), events.put(None)), daemon=True)
            worker.start()
            while True:
                ev = events.get()
                if ev is None:
                    break
                kind, data = ev
                try:
                    self.wfile.write(f'event: {kind}\ndata: {json.dumps(data)}\n\n'.encode())
                    self.wfile.flush()
                except BrokenPipeError:
                    break
            return None
        return self._send(404, b'Not found', 'text/plain')


if __name__ == '__main__':
    print(f'BVAL demo on http://localhost:{PORT}  (run page)  and  http://localhost:{PORT}/agent  (agent page)')
    backend = f'LM Studio {LMSTUDIO_MODEL} at {LMSTUDIO_URL}' if AGENT_BACKEND != 'claude' else f'Claude {MODEL}'
    print(f'Agent model: {backend}. Tool: live Apify Actor {ACTOR_ID}.')
    for var in ('APIFY_TOKEN',) + (('LM_API_TOKEN',) if AGENT_BACKEND != 'claude' else ()):
        if not os.environ.get(var):
            print(f'warning: {var} is not set; runs will fail until it is.')
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
