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

The dashboard also includes a chart of average effectiveness score per
category, and a "Compare party positions" page showing every party's stance
across all categories side by side.

A scheduled GitHub Actions workflow re-runs the data collection weekly and
commits any updates automatically, so "NEW" badges and scores stay current
without manual work.

## Project structure

- `collect_data.py` — fetches documents from GOV.UK, analyzes them with Claude,
  saves results to `data.json`
- `generate_dashboard.py` — builds the main dashboard (`index.html`)
- `generate_party_positions.py` — generates per-category party position
  briefings (`party_positions.json`) grounded in `research/party_positions_research.md`
- `generate_topic_pages.py` — builds one page per policy category
- `ask.py` — command-line Q&A tool over the tracked documents
- `server.py` — web server that serves the dashboard and adds an in-browser
  Q&A box (calls Claude via a `/api/ask` endpoint); used both locally and for
  the hosted backend deployment
- `generate_compare_page.py` — builds the "Compare party positions" page
  (`compare.html`)
- `.github/workflows/update-data.yml` — weekly scheduled job that re-runs
  data collection and commits the result

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
   python3 generate_compare_page.py
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

## Deploying the live Q&A backend

The GitHub Pages demo above is static, so its Q&A box only works when you run
`server.py` locally. To make Q&A work on a public URL too, `server.py` can be
deployed to a free host such as [Render](https://render.com):

1. Sign in to Render with your GitHub account and create a new **Web Service**
   from the `reg-radar` repo.
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn server:app`
4. Add an environment variable `ANTHROPIC_API_KEY` with your Claude API key.
5. Deploy — Render gives you a public URL serving the full dashboard with a
   working Q&A box.

## Keeping data up to date

`.github/workflows/update-data.yml` runs every Monday and re-collects the
latest policy documents. For it to work, add your Claude API key as a repo
secret: **Settings → Secrets and variables → Actions → New repository
secret**, named `ANTHROPIC_API_KEY`.

## Why I built this

I'm a recent graduate aiming for a career in tech/AI policy advisory, and I
wanted a project that combined that policy interest with practical AI/coding
skills. Reg Radar is the result: it pulls real UK government policy
documents, uses Claude to triage, score, and categorise them, and turns that
into something a policy analyst could actually use to quickly see what's
changed and where each major party stands.

Along the way I learned how to work with external APIs (GOV.UK Search,
Anthropic), structure AI output reliably (JSON parsing, prompt design),
build a simple RAG pipeline (grounding party-position summaries in real
research rather than relying on a model's training data), and ship a small
full-stack project (static dashboard + Flask backend) end-to-end, including
deployment.

## Disclaimer

Effectiveness scores and party-position briefings are AI-generated and may
not reflect the most current positions. Always verify against primary sources.
