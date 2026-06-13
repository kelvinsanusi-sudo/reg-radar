# Reg Radar

A UK tech, AI & social media policy tracker built with Claude (Anthropic API).

**Live demo:** _(add your GitHub Pages link here once deployed)_

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

## Project structure

- `collect_data.py` — fetches documents from GOV.UK, analyzes them with Claude,
  saves results to `data.json`
- `generate_dashboard.py` — builds the main dashboard (`index.html`)
- `generate_party_positions.py` — generates per-category party position
  briefings (`party_positions.json`) grounded in `research/party_positions_research.md`
- `generate_topic_pages.py` — builds one page per policy category
- `ask.py` — command-line Q&A tool over the tracked documents

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

## Disclaimer

Effectiveness scores and party-position briefings are AI-generated and may
not reflect the most current positions. Always verify against primary sources.
