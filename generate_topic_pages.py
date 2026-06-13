import json
import re

with open("data.json") as f:
    items = json.load(f)

with open("party_positions.json") as f:
    briefings = json.load(f)

CATEGORIES = [
    "AI Regulation",
    "Online Safety",
    "Data Protection & Privacy",
    "Digital Markets & Competition",
    "Social Media Regulation",
    "AI in Public Services",
]


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


PARTY_LABELS = {
    "labour": "Labour",
    "conservative": "Conservative",
    "reform": "Reform UK",
    "green": "Green Party",
    "lib_dem": "Liberal Democrats",
}

PARTY_COLORS = {
    "labour": "#e4003b",
    "conservative": "#0087dc",
    "reform": "#12b6cf",
    "green": "#02a95c",
    "lib_dem": "#faa61a",
}


def render_page(category, items_in_category, briefing):
    party_html = ""
    for key, label in PARTY_LABELS.items():
        party_html += f"""
        <div class="party-card">
          <div class="party-name" style="border-color:{PARTY_COLORS[key]}">{label}</div>
          <p>{briefing[key]}</p>
        </div>"""

    docs_html = ""
    for item in items_in_category:
        docs_html += f"""
        <div class="card">
          <div class="card-body">
            <h2>{item['title']}</h2>
            <div class="meta">{item['date']} &middot; Effectiveness score: {item['effectiveness_score']}</div>
            <p class="field summary">{item['summary']}</p>
            <a class="doc-link" href="{item['link']}" target="_blank">View original document &rarr;</a>
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{category} - Reg Radar</title>
  <style>
    :root {{
      --accent: #5b5fec;
      --accent-light: #eef0ff;
      --text-main: #1d1d1f;
      --text-muted: #8a8a8e;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, "Segoe UI", Inter, Arial, sans-serif;
      margin: 0;
      padding: 2.5rem 2rem 4rem;
      background: linear-gradient(180deg, #f7f7fb 0%, #eef0f6 100%);
      color: var(--text-main);
    }}
    .container {{ max-width: 820px; margin: 0 auto; }}
    a.back {{
      display: inline-block;
      margin-bottom: 1rem;
      color: var(--accent);
      text-decoration: none;
      font-weight: 600;
      font-size: 0.9rem;
    }}
    h1 {{ margin: 0 0 0.4rem; font-size: 2rem; letter-spacing: -0.02em; }}
    .subtitle {{ color: var(--text-muted); margin: 0 0 1.8rem; font-size: 0.95rem; }}

    .trend-box {{
      background: var(--accent-light);
      border-radius: 14px;
      padding: 1.2rem 1.5rem;
      margin-bottom: 1.5rem;
      font-size: 0.95rem;
      line-height: 1.5;
    }}
    .party-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 0.8rem;
      margin-bottom: 2.5rem;
    }}
    .party-card {{
      background: white;
      border-radius: 12px;
      padding: 1rem 1.2rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      font-size: 0.85rem;
      line-height: 1.45;
    }}
    .party-name {{
      font-weight: 700;
      margin-bottom: 0.4rem;
      padding-left: 0.6rem;
      border-left: 4px solid;
    }}
    .disclaimer {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-bottom: 2rem;
      font-style: italic;
    }}
    .card {{
      background: white;
      border-radius: 14px;
      padding: 1.4rem 1.5rem;
      margin-bottom: 1rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .card h2 {{ margin: 0 0 0.5rem 0; font-size: 1.05rem; font-weight: 600; line-height: 1.35; }}
    .meta {{
      font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.8rem;
      text-transform: uppercase; letter-spacing: 0.04em;
    }}
    .summary {{ color: #444; }}
    a.doc-link {{ color: var(--accent); font-weight: 600; font-size: 0.88rem; text-decoration: none; }}
    a.doc-link:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="container">
    <a class="back" href="index.html">&larr; Back to dashboard</a>
    <h1>{category}</h1>
    <div class="subtitle">Government trend &amp; party positions, plus tracked documents in this area</div>

    <div class="trend-box">{briefing['trend_summary']}</div>

    <div class="party-grid">{party_html}
    </div>
    <div class="disclaimer">
      Party positions are AI-generated from web research as of June 2026 and may not reflect
      the latest statements. Always verify against primary sources before relying on this.
    </div>

    <h3>Tracked documents ({len(items_in_category)})</h3>
    {docs_html}
  </div>
</body>
</html>
"""


for category in CATEGORIES:
    items_in_category = [i for i in items if category in i.get("categories", [])]
    # Sort by effectiveness score, highest first
    items_in_category.sort(key=lambda x: x["effectiveness_score"], reverse=True)

    html = render_page(category, items_in_category, briefings[category])
    filename = f"topic-{slugify(category)}.html"
    with open(filename, "w") as f:
        f.write(html)
    print(f"Wrote {filename} ({len(items_in_category)} documents)")
