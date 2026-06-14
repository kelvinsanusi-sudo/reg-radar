import os
import json
from dotenv import load_dotenv
import anthropic
from flask import Flask, request, jsonify, send_from_directory

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


app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)


@app.route("/api/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}],
    )
    return jsonify({"answer": response.content[0].text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
