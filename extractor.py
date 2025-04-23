from bs4 import BeautifulSoup
import re
import requests

def extract_facts_from_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=" ").strip()

    # Extract only clean factual sentences (simple heuristic)
    sentences = re.findall(r'([A-Z][^.!?]{20,150}[.!?])', text)
    return [s.strip() for s in sentences if len(s.split()) > 5]

facts = extract_facts_from_url("https://en.wikipedia.org/wiki/Chemical_industry")
for fact in facts[:10]:
    print("-", fact)
