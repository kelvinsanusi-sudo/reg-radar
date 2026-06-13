import os
import json
import datetime
import requests
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Search terms covering UK tech/AI/social media policy
SEARCH_TERMS = [
    "artificial intelligence",
    "online safety",
    "social media regulation",
    "data protection",
    "AI safety",
    "digital markets",
]

# GOV.UK document types that tend to be actual policy content
DOC_TYPES = ["policy_paper", "guidance"]

DOCS_PER_SEARCH = 8

# Fixed set of broad categories used for grouping/tagging documents
CATEGORIES = [
    "AI Regulation",
    "Online Safety",
    "Data Protection & Privacy",
    "Digital Markets & Competition",
    "Social Media Regulation",
    "AI in Public Services",
]

CATEGORY_LIST_TEXT = "\n".join(f"- {c}" for c in CATEGORIES)

PROMPT_TEMPLATE = """You are a policy analyst assistant. You will be given the title and
description of a UK government policy/guidance document. Decide whether it is
relevant to technology, AI, or social media policy.

If relevant, score it on three dimensions, each 0-100:
- clarity_score: how clear and unambiguous are the requirements?
- enforceability_score: how enforceable are these requirements in practice (penalties, monitoring, etc.)?
- scope_score: how broad/significant is the impact if implemented (more impact = higher score)?

Then give an overall effectiveness_score (0-100) that reflects your holistic
judgement of how likely this policy is to achieve its stated goals, informed
by (but not necessarily a simple average of) the three dimension scores above.

If relevant, also assign 1-3 categories from this fixed list (use the exact
strings, choose only ones that genuinely apply):
""" + CATEGORY_LIST_TEXT + """

Respond with ONLY valid JSON (no other text, no markdown formatting) in exactly
this format:
{{
  "relevant": true or false,
  "topic": "short specific topic label, e.g. 'AI transparency requirements', or 'not tech-related'",
  "categories": ["one or more of the fixed categories above"], or [] if not relevant,
  "affected_parties": "who this impacts, e.g. 'AI model providers', or 'none' if not relevant",
  "clarity_score": integer 0-100, or 0 if not relevant,
  "enforceability_score": integer 0-100, or 0 if not relevant,
  "scope_score": integer 0-100, or 0 if not relevant,
  "effectiveness_score": integer 0-100, or 0 if not relevant,
  "score_reasoning": "1-2 sentence explanation of the overall effectiveness score, or 'n/a' if not relevant",
  "summary": "1-2 sentence plain-English summary"
}}

Title: {title}
Description: {description}
"""


def fetch_documents(term):
    all_results = []
    for doc_type in DOC_TYPES:
        url = "https://www.gov.uk/api/search.json"
        params = {
            "q": term,
            "count": DOCS_PER_SEARCH,
            "filter_content_store_document_type": doc_type,
            "fields": "title,description,link,public_timestamp",
        }
        response = requests.get(url, params=params)
        all_results.extend(response.json().get("results", []))
    return all_results


def analyze_document(doc):
    prompt = PROMPT_TEMPLATE.format(
        title=doc["title"], description=doc.get("description", "")
    )
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    raw_text = response.content[0].text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return None


def load_previous_first_seen():
    """Read the existing data.json (if any) and return {link: first_seen_date}."""
    if not os.path.exists("data.json"):
        return {}
    with open("data.json") as f:
        previous_items = json.load(f)
    return {item["link"]: item.get("first_seen") for item in previous_items}


def main():
    today = datetime.date.today().isoformat()
    previous_first_seen = load_previous_first_seen()

    seen_links = set()
    results = []

    for term in SEARCH_TERMS:
        print(f"Searching for: {term}")
        docs = fetch_documents(term)

        for doc in docs:
            link = doc["link"]
            full_link = "https://www.gov.uk" + link
            if link in seen_links:
                continue
            seen_links.add(link)

            analysis = analyze_document(doc)
            if analysis is None or not analysis.get("relevant"):
                continue

            # If we've seen this link before, keep its original "first seen"
            # date (falling back to publication date if not tracked yet).
            # Otherwise, it's new as of today.
            if full_link in previous_first_seen:
                first_seen = previous_first_seen[full_link] or doc.get("public_timestamp", "")[:10] or today
            else:
                first_seen = today

            results.append({
                "title": doc["title"],
                "date": doc.get("public_timestamp", "")[:10],
                "link": full_link,
                "topic": analysis["topic"],
                "categories": analysis.get("categories", []),
                "affected_parties": analysis["affected_parties"],
                "clarity_score": analysis.get("clarity_score", 0),
                "enforceability_score": analysis.get("enforceability_score", 0),
                "scope_score": analysis.get("scope_score", 0),
                "effectiveness_score": analysis["effectiveness_score"],
                "score_reasoning": analysis["score_reasoning"],
                "summary": analysis["summary"],
                "first_seen": first_seen,
                "is_new": first_seen == today,
            })
            print(f"  + [{analysis['effectiveness_score']}] {doc['title'][:60]}...")

    # Sort by effectiveness score, highest first
    results.sort(key=lambda x: x["effectiveness_score"], reverse=True)

    with open("data.json", "w") as f:
        json.dump(results, f, indent=2)

    new_count = sum(1 for r in results if r["is_new"])
    print(f"\nSaved {len(results)} relevant items to data.json ({new_count} new since last run)")


if __name__ == "__main__":
    main()
