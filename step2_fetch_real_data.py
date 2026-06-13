import requests

# Federal Register's public search API - no API key needed
url = "https://www.federalregister.gov/api/v1/articles.json"
params = {
    "conditions[term]": "artificial intelligence",
    "conditions[type][]": "RULE",
    "order": "newest",
    "per_page": 5,
    "fields[]": ["title", "abstract", "publication_date", "html_url"],
}

response = requests.get(url, params=params)
data = response.json()

print(f"Found {data['count']} total results. Showing the {len(data['results'])} most recent:\n")

for doc in data["results"]:
    print("=" * 60)
    print(f"Title: {doc['title']}")
    print(f"Date: {doc['publication_date']}")
    print(f"Abstract: {doc['abstract']}")
    print(f"Link: {doc['html_url']}")
    print()
