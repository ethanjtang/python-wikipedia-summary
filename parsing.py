import requests
from bs4 import BeautifulSoup
import re

def parse_wikipedia_json(json_data):
    parsed_text = ""
    if 'parse' in json_data:
        page = json_data['parse']
        if 'text' in page and '*' in page['text']:
            # The content is in HTML format, we need to parse it
            html_content = page['text']['*']
            soup = BeautifulSoup(html_content, 'html.parser')
            paragraphs = soup.find_all('p')
            for para in paragraphs:
                parsed_text += para.get_text() + "\n\n"
    return parsed_text.strip()

def clean_wikipedia_text(parsed_json_content):
    text = parsed_json_content

    # Remove Wikipedia citation brackets (e.g., [1], [2], etc.)
    text = re.sub(r'\[\d+\]', '', text)

    # Remove nested citation brackets
    text = re.sub(r'\[[a-z]\]', '', text)

    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)

    # Remove any unwanted special characters or excessive whitespace
    text = re.sub(r'\s{2,}', ' ', text)

    # Correct paragraph breaks by ensuring there is only one newline between paragraphs
    paragraphs = text.split('\n')
    cleaned_paragraphs = []
    
    for paragraph in paragraphs:
        if paragraph.strip():  # Ignore empty lines
            cleaned_paragraphs.append(paragraph.strip())
    
    cleaned_text = '\n\n'.join(cleaned_paragraphs)
    
    return cleaned_text

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "parse",
    "page": "Ice cream",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

# print(DATA["parse"]["text"]["*"])
print(clean_wikipedia_text(parse_wikipedia_json(DATA)))

# TODO: When parsing equations, the formatting gets messed up really badly (ex. page on icecream). Would like to fix this for readibility and to decrease number of tokens
# when feeding this to ChatGPT