import os
from dotenv import load_dotenv
import anthropic

# Load the ANTHROPIC_API_KEY from our .env file into the environment
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# A short sample of "regulatory text" to summarize
sample_text = """
The proposed amendment to the AI Act introduces new transparency requirements
for providers of general-purpose AI models. Providers must publish a summary
of training data sources, document known limitations, and disclose energy
consumption during training. Non-compliance may result in fines of up to 3%
of global annual turnover. The requirements apply to any model placed on the
market within the EU, regardless of where the provider is based.
"""

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=200,
    messages=[
        {
            "role": "user",
            "content": f"Summarize the following regulatory text in 2-3 plain-English sentences:\n\n{sample_text}",
        }
    ],
)

print("=== Claude's Summary ===")
print(response.content[0].text)
