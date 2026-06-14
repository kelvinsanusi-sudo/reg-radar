import json
import re


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


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

header_html = "".join(
    f'<th style="border-bottom:3px solid {PARTY_COLORS[key]}">{label}</th>'
    for key, label in PARTY_LABELS.items()
)

rows_html = ""
for category in CATEGORIES:
    briefing = briefings[category]
    cells = "".join(
        f"<td>{briefing[key]}</td>" for key in PARTY_LABELS
    )
    rows_html += f"""
    <tr>
      <td class="category-cell"><a href="topic-{slugify(category)}.html">{category}</a></td>
      {cells}
    </tr>"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Compare party positions - Reg Radar</title>
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
    .container {{ max-width: 1200px; margin: 0 auto; }}
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
    .table-wrap {{
      overflow-x: auto;
      background: white;
      border-radius: 14px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      margin-bottom: 1.5rem;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      font-size: 0.85rem;
    }}
    th, td {{
      text-align: left;
      vertical-align: top;
      padding: 0.9rem 1rem;
      border-bottom: 1px solid #eee;
      min-width: 200px;
    }}
    th {{
      background: var(--accent-light);
      font-weight: 700;
      white-space: nowrap;
    }}
    .category-cell {{
      font-weight: 700;
      background: var(--accent-light);
      min-width: 180px;
    }}
    .category-cell a {{
      color: var(--text-main);
      text-decoration: none;
    }}
    .category-cell a:hover {{
      color: var(--accent);
    }}
    .disclaimer {{
      font-size: 0.78rem;
      color: var(--text-muted);
      font-style: italic;
    }}
  </style>
</head>
<body>
  <div class="container">
    <a class="back" href="index.html">&larr; Back to dashboard</a>
    <h1>Compare party positions</h1>
    <div class="subtitle">Side-by-side view of all major UK parties' positions across every policy category</div>

    <div class="table-wrap">
      <table>
        <tr>
          <th>Category</th>
          {header_html}
        </tr>
        {rows_html}
      </table>
    </div>

    <div class="disclaimer">
      Party positions are AI-generated from web research as of June 2026 and may not reflect
      the latest statements. Always verify against primary sources before relying on this.
    </div>
  </div>
</body>
</html>
"""

with open("compare.html", "w") as f:
    f.write(html)

print("Wrote compare.html")
