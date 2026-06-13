import os
import json
import re
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

CATEGORIES = [
    "AI Regulation",
    "Online Safety",
    "Data Protection & Privacy",
    "Digital Markets & Competition",
    "Social Media Regulation",
    "AI in Public Services",
]

PROMPT_TEMPLATE = """You are a UK policy analyst. Using ONLY the research notes
below (do not add information from your own memory beyond what's given), write
a briefing on the policy area "{category}".

Research notes:
---
{research}
---

Respond with ONLY valid JSON (no markdown formatting) in this exact format:
{{
  "trend_summary": "2-3 sentences on the overall government direction/trend in this area",
  "labour": "1-2 sentences on Labour's position, or 'No clear position found in research' if not covered",
  "conservative": "1-2 sentences on the Conservative position, or 'No clear position found in research'",
  "reform": "1-2 sentences on Reform UK's position, or 'No clear position found in research'",
  "green": "1-2 sentences on the Green Party's position, or 'No clear position found in research'",
  "lib_dem": "1-2 sentences on the Liberal Democrats' position, or 'No clear position found in research'"
}}
"""


def split_research_by_category(text):
    """Split the markdown research file into sections keyed by category heading."""
    sections = {}
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    # parts[0] is the intro before the first heading; then alternates heading, body
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1].strip()
        sections[heading] = body
    return sections


def generate_briefing(category, research_text):
    prompt = PROMPT_TEMPLATE.format(category=category, research=research_text)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    raw_text = response.content[0].text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()
    return json.loads(raw_text)


def main():
    with open("research/party_positions_research.md") as f:
        research_text = f.read()

    sections = split_research_by_category(research_text)

    briefings = {}
    for category in CATEGORIES:
        research_section = sections.get(category, "No research available.")
        print(f"Generating briefing for: {category}")
        briefings[category] = generate_briefing(category, research_section)

    with open("party_positions.json", "w") as f:
        json.dump(briefings, f, indent=2)

    print("\nSaved briefings to party_positions.json")


if __name__ == "__main__":
    main()
