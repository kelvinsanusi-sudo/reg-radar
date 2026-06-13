import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

with open("data.json") as f:
    items = json.load(f)


def build_context():
    """Turn our tracked documents into a text block Claude can use as context."""
    lines = []
    for i, item in enumerate(items, start=1):
        lines.append(
            f"[{i}] Title: {item['title']}\n"
            f"    Date: {item['date']}\n"
            f"    Categories: {', '.join(item['categories'])}\n"
            f"    Affected parties: {item['affected_parties']}\n"
            f"    Effectiveness score: {item['effectiveness_score']}/100\n"
            f"    Summary: {item['summary']}\n"
            f"    Link: {item['link']}"
        )
    return "\n\n".join(lines)


SYSTEM_PROMPT = """You are a policy research assistant for Reg Radar, a tracker of
UK tech/AI/social media policy documents. Answer the user's question using ONLY
the tracked documents provided below as context. If the documents don't contain
enough information to answer, say so clearly rather than guessing.

When you use information from a document, cite it using its [number] reference.

Tracked documents:
""" + build_context()


def main():
    print("Reg Radar Q&A — ask a question about tracked UK tech/AI policy (or 'quit' to exit)\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if not question:
            continue

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": question}],
        )
        print(f"\nClaude: {response.content[0].text}\n")


if __name__ == "__main__":
    main()
