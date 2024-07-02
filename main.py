import api_key

import math
import os
import re
import requests
import wikipedia

from bs4 import BeautifulSoup
from openai import OpenAI


def parse_wikipedia_json(json_data):
    parsed_text = ""
    if 'parse' in json_data:
        page = json_data['parse']
        if 'text' in page and '*' in page['text']:
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
        api_key=api_key.OPENAI_API_KEY,
    )

    prompt = load_prompt("food")

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

    return gpt_summary

def combine_summaries(summaries):
    f = open(r"prompts/test2.txt", "r")
    prompt = f.read()
    f.close()

    paragraph_num = 1

    for summary in summaries:
        prompt += "Summary #" + str(paragraph_num) + ":" + "\n"
        prompt += summary
        prompt += "\n"
        paragraph_num += 1
    

    client = OpenAI(
        api_key=api_key.OPENAI_API_KEY,
    )

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="gpt-3.5-turbo",
    )

    summary_squared = chat_completion.choices[0].message.content

    return summary_squared
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

def load_prompt(topic):
    f = open(r"prompts/test.txt", "r")
    prompt = f.read()
    f.close
    return prompt

def split_string(page_content):
    split_string = []
    
    words = page_content.split()
    
    # Create a list to hold the chunks
    chunks = []
    
    # Loop through the words and create chunks
    for i in range(0, len(words), 10000):
        chunk = words[i:i + 10000]
        chunks.append(" ".join(chunk))
    
    for element in chunks:
        print("\n")
        print(element)
        print("\n")
    return chunks



user_query = input("Please input a topic you wish to learn more about:\n")
topic = search_wikipedia_page(user_query)
page_content = get_wikipedia_page_content(topic)
chunked_page_content = []

word_count = page_content.count(" ")
est_token_count = word_count * 1.5
print(word_count)
print("Estimated token count: " + str(int(est_token_count)))

if (est_token_count > 16000):
    num_splits = math.ceil(est_token_count / 15000)
    print("Number of splits needed: " + str(num_splits))
    chunked_page_content = split_string(page_content)

if (num_splits < 2):
    gpt_summary = summarize_wikipedia_page(page_content)
    print(gpt_summary)
else:
    for i in range(num_splits):
        chunked_summaries = []
        chunk = summarize_wikipedia_page(chunked_page_content[i])
        print("Summary #" + str(i + 1))
        print(chunk)
        chunked_summaries.append(chunk)

    gpt_summary = combine_summaries(chunked_summaries)
    print("Final summary:\n")
    print(gpt_summary)



# 

# res_first = test_str[0:len(test_str)//2] 