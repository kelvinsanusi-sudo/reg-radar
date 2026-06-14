# Reg Radar

A UK tech, AI & social media policy tracker built with Claude (Anthropic API).

**Live demo:** https://kelvinsanusi-sudo.github.io/reg-radar/

## What it does

Reg Radar pulls real UK government policy documents (via the GOV.UK Search API),
uses Claude to:

- Triage which documents are actually relevant to tech/AI/social media policy
- Score each document's likely **effectiveness** (0-100), broken down into
  clarity, enforceability, and scope
- Tag each document with one or more policy **categories**
- Track which documents are **new** since the last run

It then presents this as a searchable, filterable dashboard, with dedicated
pages per category showing the overall government trend and a summary of
each major UK party's position (generated via web research as grounding
context — a simple example of Retrieval-Augmented Generation).

A command-line tool (`ask.py`) lets you ask natural-language questions about
the tracked documents, with Claude citing specific sources in its answers.
There's also an in-browser version of this Q&A box (`server.py`) — see below.

## Project structure

- `collect_data.py` — fetches documents from GOV.UK, analyzes them with Claude,
  saves results to `data.json`
- `generate_dashboard.py` — builds the main dashboard (`index.html`)
- `generate_party_positions.py` — generates per-category party position
  briefings (`party_positions.json`) grounded in `research/party_positions_research.md`
- `generate_topic_pages.py` — builds one page per policy category
- `ask.py` — command-line Q&A tool over the tracked documents
- `server.py` — local web server that adds an in-browser Q&A box to the
  dashboard (calls Claude via a `/api/ask` endpoint)

## Running it locally

1. Install dependencies:
   ```
   pip3 install -r requirements.txt
   ```
2. Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
3. Run the pipeline:
   ```
   python3 collect_data.py
   python3 generate_party_positions.py
   python3 generate_topic_pages.py
   python3 generate_dashboard.py
   ```
4. Open `index.html` in your browser, or ask questions with:
   ```
   python3 ask.py
   ```
5. For the in-browser Q&A box, run the local server instead of opening
   `index.html` directly:
   ```
   python3 server.py
   ```
   Then visit http://127.0.0.1:5000 — the "Ask a question" box on the
   dashboard will work. Note: this only works locally, since GitHub Pages
   (used for the live demo) can't run a Python backend.

## Disclaimer

Effectiveness scores and party-position briefings are AI-generated and may
not reflect the most current positions. Always verify against primary sources.
