import os
import json
import requests
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# --- Step A: fetch a few real documents (same as Phase 2) ---
url = "https://www.federalregister.gov/api/v1/articles.json"
params = {
    "conditions[term]": "artificial intelligence",
    "conditions[type][]": "RULE",
    "order": "newest",
    "per_page": 5,
    "fields[]": ["title", "abstract", "publication_date", "html_url"],
}
response = requests.get(url, params=params)
documents = response.json()["results"]

# --- Step B: the instructions we give Claude for every document ---
PROMPT_TEMPLATE = """You are a policy analyst assistant. You will be given the title and
abstract of a government regulatory document. Decide whether it is relevant to
technology, AI, or social media policy.

Respond with ONLY valid JSON (no other text, no markdown formatting) in exactly
this format:
{{
  "relevant": true or false,
  "topic": "short topic label, e.g. 'AI transparency' or 'not tech-related'",
  "affected_parties": "who this impacts, e.g. 'AI model providers', or 'none' if not relevant",
  "risk_level": "low, medium, or high - only set if relevant, otherwise 'n/a'",
  "summary": "1-2 sentence plain-English summary"
}}

Title: {title}
Abstract: {abstract}
"""

# --- Step C: ask Claude about each document ---
for doc in documents:
    prompt = PROMPT_TEMPLATE.format(title=doc["title"], abstract=doc["abstract"])

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text.strip()

    # Claude sometimes wraps JSON in markdown code fences (```json ... ```)
    # Strip those off before parsing
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        print(f"Could not parse response for: {doc['title'][:60]}...")
        print("Raw response:", raw_text)
        continue

    print("=" * 60)
    print(f"Title: {doc['title'][:80]}")
    print(f"Relevant to tech/AI policy? {result['relevant']}")
    if result["relevant"]:
        print(f"Topic: {result['topic']}")
        print(f"Affected: {result['affected_parties']}")
        print(f"Risk level: {result['risk_level']}")
        print(f"Summary: {result['summary']}")
    print()
