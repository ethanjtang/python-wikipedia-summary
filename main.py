import os
import requests
import re
import wikipedia

from bs4 import BeautifulSoup
from openai import OpenAI

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

def search_wikipedia_page(user_query):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    search = user_query

    SEARCHPAGE = search

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": SEARCHPAGE
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    '''
        for i in range(10):
        print(DATA['query']['search'][i]['title'])
    '''

    return DATA['query']['search'][0]['title']

def summarize_wikipedia_page(page_content):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    prompt = "Please provide me a detailed summary of the contents of this Wikipedia page. In this summary, make sure to include the following details: 1. Name of the food\n 2. Other names for the food\n 3. Where/When/Why the food was invented\n 4. Who invented the food and how it became popular\n 5. The recipe/process to create the food\n 6. Other related foodstuffs and recipes\n Please format your short summary as multiple paragraphs instead of a bulleted or numbered list. It should flow naturally like a summary of the topic on Wikipedia."

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt + "Wikipedia page content:\n" + page_content,
        }
    ],
    model="gpt-3.5-turbo",
    )

    gpt_summary = chat_completion.choices[0].message.content

    return "Wikipedia page summarized by GPT-4:\n" + gpt_summary

def get_wikipedia_page_content(topic):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "parse",
        "page": topic,
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    page_content = clean_wikipedia_text(parse_wikipedia_json(DATA))

    return page_content

user_query = input("Please input a topic you wish to learn more about:\n")
topic = search_wikipedia_page(user_query)
# print("Topic identified:" + topic)
page_content = get_wikipedia_page_content(topic)
# print("Page content:" + page_content + "\n")
gpt_summary = summarize_wikipedia_page(page_content)
print(gpt_summary)

