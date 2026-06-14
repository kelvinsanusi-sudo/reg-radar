import json
import re


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


with open("data.json") as f:
    items = json.load(f)

data_json_string = json.dumps(items)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Reg Radar - UK Tech & AI Policy Dashboard</title>
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
    .container {{
      max-width: 820px;
      margin: 0 auto;
    }}
    h1 {{
      margin: 0;
      font-size: 2.2rem;
      letter-spacing: -0.02em;
    }}
    .subtitle {{
      color: var(--text-muted);
      margin: 0.3rem 0 1.8rem;
      font-size: 0.95rem;
    }}
    .controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.8rem;
      margin-bottom: 2rem;
    }}
    #search, #companyFilter {{
      padding: 0.75rem 1rem;
      font-size: 0.95rem;
      border: 1px solid #ddd;
      border-radius: 10px;
      background: white;
      box-shadow: 0 1px 2px rgba(0,0,0,0.03);
      outline: none;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    #search {{
      flex: 1;
      min-width: 220px;
      max-width: 420px;
    }}
    #companyFilter {{
      min-width: 220px;
    }}
    #companyFilter:focus, #search:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-light);
    }}
    .ask-box {{
      background: white;
      border-radius: 14px;
      padding: 1.2rem 1.5rem;
      margin-bottom: 2rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .ask-box h3 {{
      margin: 0 0 0.6rem;
      font-size: 1rem;
      color: var(--text-main);
    }}
    .ask-box .ask-row {{
      display: flex;
      gap: 0.6rem;
    }}
    #askInput {{
      flex: 1;
      padding: 0.75rem 1rem;
      font-size: 0.95rem;
      border: 1px solid #ddd;
      border-radius: 10px;
      outline: none;
    }}
    #askInput:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-light);
    }}
    #askButton {{
      background: var(--accent);
      color: white;
      border: none;
      border-radius: 10px;
      padding: 0.75rem 1.4rem;
      font-size: 0.95rem;
      cursor: pointer;
    }}
    #askButton:disabled {{
      opacity: 0.6;
      cursor: default;
    }}
    #askAnswer {{
      margin-top: 1rem;
      line-height: 1.5;
      white-space: pre-wrap;
    }}
    #askNote {{
      margin-top: 0.6rem;
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    .card {{
      background: white;
      border-radius: 14px;
      padding: 1.4rem 1.5rem;
      margin-bottom: 1rem;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      display: flex;
      gap: 1.2rem;
      align-items: flex-start;
      transition: box-shadow 0.15s ease, transform 0.15s ease;
    }}
    .card:hover {{
      box-shadow: 0 6px 20px rgba(0,0,0,0.08);
      transform: translateY(-1px);
    }}
    .card-body {{
      flex: 1;
      min-width: 0;
    }}
    .card h2 {{
      margin: 0 0 0.5rem 0;
      font-size: 1.05rem;
      font-weight: 600;
      line-height: 1.35;
    }}
    .meta {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-bottom: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .field {{
      margin: 0.5rem 0;
      font-size: 0.92rem;
      line-height: 1.5;
    }}
    .field-label {{
      display: inline-block;
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--accent);
      margin-right: 0.4rem;
    }}
    .topic-tag {{
      display: inline-block;
      background: var(--accent-light);
      color: var(--accent);
      font-weight: 600;
      font-size: 0.8rem;
      padding: 0.25rem 0.7rem;
      border-radius: 999px;
      text-decoration: none;
      transition: background 0.15s ease;
      margin: 0.15rem 0.25rem 0.15rem 0;
    }}
    .topic-tag:hover {{
      background: var(--accent);
      color: white;
    }}
    .summary {{
      color: #444;
    }}
    a.doc-link {{
      color: var(--accent);
      font-weight: 600;
      font-size: 0.88rem;
      text-decoration: none;
    }}
    a.doc-link:hover {{
      text-decoration: underline;
    }}

    /* Score badge + tooltip */
    .score-wrap {{
      position: relative;
      flex-shrink: 0;
    }}
    .score-badge {{
      width: 52px;
      height: 52px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 1.05rem;
      color: white;
      cursor: default;
      box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }}
    .tooltip {{
      visibility: hidden;
      opacity: 0;
      position: absolute;
      top: 110%;
      left: 0;
      width: 240px;
      background: #1d1d1f;
      color: white;
      padding: 0.7rem 0.9rem;
      border-radius: 8px;
      font-size: 0.8rem;
      line-height: 1.4;
      z-index: 10;
      transition: opacity 0.15s ease;
      box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }}
    .score-breakdown {{
      margin-top: 0.5rem;
      padding-top: 0.5rem;
      border-top: 1px solid rgba(255,255,255,0.2);
      display: flex;
      justify-content: space-between;
      gap: 0.4rem;
      font-size: 0.72rem;
      color: #ccc;
    }}
    .score-breakdown div {{ text-align: center; }}
    .score-breakdown span {{
      display: block;
      font-weight: 700;
      color: white;
      font-size: 0.85rem;
    }}
    .new-badge {{
      display: inline-block;
      background: #ff3b30;
      color: white;
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      padding: 0.15rem 0.5rem;
      border-radius: 999px;
      vertical-align: middle;
      margin-left: 0.4rem;
    }}
    .score-wrap:hover .tooltip {{
      visibility: visible;
      opacity: 1;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Reg Radar</h1>
    <div class="subtitle">UK Tech, AI & Social Media Policy Tracker — sorted by effectiveness score</div>

    <div class="ask-box">
      <h3>Ask a question about tracked policy documents</h3>
      <div class="ask-row">
        <input type="text" id="askInput" placeholder="e.g. What is the government doing about AI in schools?">
        <button id="askButton">Ask</button>
      </div>
      <div id="askAnswer"></div>
      <div id="askNote">Powered by Claude. Only works when running locally via <code>python3 server.py</code>.</div>
    </div>

    <div class="controls">
      <input type="text" id="search" placeholder="Search by topic, summary, or affected parties...">
      <select id="companyFilter">
        <option value="all">All company types</option>
        <option value="ai">AI model providers / developers</option>
        <option value="social">Social media / online platforms</option>
        <option value="data">Data controllers &amp; processors (general business)</option>
        <option value="digital_markets">Large digital platforms (Strategic Market Status)</option>
        <option value="public_sector">Public sector / government bodies</option>
      </select>
    </div>

    <div id="results"></div>
  </div>

  <script>
    const items = {data_json_string};
    const resultsDiv = document.getElementById('results');
    const searchBox = document.getElementById('search');

    function scoreColor(score) {{
      const hue = (score / 100) * 120;
      return `hsl(${{hue}}, 70%, 45%)`;
    }}

    function slugify(text) {{
      return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
    }}

    function render(filteredItems) {{
      resultsDiv.innerHTML = '';
      filteredItems.forEach(item => {{
        const card = document.createElement('div');
        card.className = 'card';
        const color = scoreColor(item.effectiveness_score);
        const newBadge = item.is_new ? '<span class="new-badge">NEW</span>' : '';
        card.innerHTML = `
          <div class="score-wrap">
            <div class="score-badge" style="background:${{color}}">${{item.effectiveness_score}}</div>
            <div class="tooltip">
              <strong>Why this score?</strong><br>${{item.score_reasoning}}
              <div class="score-breakdown">
                <div>Clarity <span>${{item.clarity_score}}</span></div>
                <div>Enforceability <span>${{item.enforceability_score}}</span></div>
                <div>Scope <span>${{item.scope_score}}</span></div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <h2>${{item.title}} ${{newBadge}}</h2>
            <div class="meta">${{item.date}} &middot; ${{item.topic}}</div>
            <div class="field">
              <span class="field-label">Categories</span>
              ${{item.categories.map(c => `<a class="topic-tag" href="topic-${{slugify(c)}}.html">${{c}}</a>`).join(' ')}}
            </div>
            <div class="field">
              <span class="field-label">Affected</span>${{item.affected_parties}}
            </div>
            <p class="field summary">${{item.summary}}</p>
            <a class="doc-link" href="${{item.link}}" target="_blank">View original document &rarr;</a>
          </div>
        `;
        resultsDiv.appendChild(card);
      }});
    }}

    // Keywords used to match each company type against an item's text
    const COMPANY_KEYWORDS = {{
      ai: ['ai', 'artificial intelligence', 'algorithm', 'model'],
      social: ['social media', 'platform', 'online safety', 'content', 'user-generated'],
      data: ['data', 'privacy', 'gdpr', 'processing', 'personal information'],
      digital_markets: ['digital market', 'competition', 'strategic market status', 'big tech'],
      public_sector: ['public sector', 'government', 'public services', 'local authorit'],
    }};

    const companyFilter = document.getElementById('companyFilter');

    function itemText(item) {{
      return [item.title, item.topic, item.summary, item.affected_parties, ...item.categories]
        .join(' ').toLowerCase();
    }}

    function applyFilters() {{
      const query = searchBox.value.toLowerCase();
      const companyType = companyFilter.value;

      const filtered = items.filter(item => {{
        const text = itemText(item);

        const matchesSearch = !query || text.includes(query);

        let matchesCompany = true;
        if (companyType !== 'all') {{
          const keywords = COMPANY_KEYWORDS[companyType];
          matchesCompany = keywords.some(kw => text.includes(kw));
        }}

        return matchesSearch && matchesCompany;
      }});
      render(filtered);
    }}

    searchBox.addEventListener('input', applyFilters);
    companyFilter.addEventListener('change', applyFilters);

    // Q&A box (only works when served by server.py, since it calls /api/ask)
    const askInput = document.getElementById('askInput');
    const askButton = document.getElementById('askButton');
    const askAnswer = document.getElementById('askAnswer');

    async function askQuestion() {{
      const question = askInput.value.trim();
      if (!question) return;

      askButton.disabled = true;
      askAnswer.textContent = 'Thinking...';

      try {{
        const res = await fetch('/api/ask', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ question }}),
        }});
        if (!res.ok) throw new Error('Request failed');
        const data = await res.json();
        askAnswer.textContent = data.answer;
      }} catch (err) {{
        askAnswer.textContent = 'Could not reach the Q&A server. Make sure you started it with: python3 server.py';
      }} finally {{
        askButton.disabled = false;
      }}
    }}

    askButton.addEventListener('click', askQuestion);
    askInput.addEventListener('keydown', e => {{
      if (e.key === 'Enter') askQuestion();
    }});

    render(items);
  </script>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)

print("Dashboard written to index.html")
