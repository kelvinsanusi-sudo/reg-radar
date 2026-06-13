import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the GEMINI_API_KEY from our .env file into the environment
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# A short sample of "regulatory text" to summarize
sample_text = """
The proposed amendment to the AI Act introduces new transparency requirements
for providers of general-purpose AI models. Providers must publish a summary
of training data sources, document known limitations, and disclose energy
consumption during training. Non-compliance may result in fines of up to 3%
of global annual turnover. The requirements apply to any model placed on the
market within the EU, regardless of where the provider is based.
"""

model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(
    f"Summarize the following regulatory text in 2-3 plain-English sentences:\n\n{sample_text}"
)

print("=== Gemini's Summary ===")
print(response.text)
