from openai import OpenAI
import os

import wikipedia

topic = input("Please enter the name of the Wikipedia page you would like to summarize: \n")

search = wikipedia.search(topic, results = 5)

if not search:
    print("No Wikipedia page found for the topic. \n")
    exit()

print("Top 5 results from search: \n")
print(search)

try:
    page = wikipedia.page(search[0], auto_suggest=False)
except wikipedia.exceptions.DisambiguationError as e:
    print(f"Disambiguation page found for '{search[0]}': {e.options}")
    exit()
except wikipedia.exceptions.PageError:
    print(f"Page not found for '{search[0]}'.")
    exit()

print("Page fetched:\n")
print(page)

print("Wikipedia summary: \n")
print(wikipedia.summary(page) + "\n")

# TODO: Fix content formatting when fetching page. Some bullet points/graphs/tables are missing and there is a lot of whitespace.
# TODO: Fix issues with length, do iterative summaries by splitting longer page into multiple requests.

'''

print("Length of wikipedia page:")
print(len(page.content))
print(page.content)

if(len(page.content) > 10):
    print("WEEWOOWEEWOO")
else:
    print("daijobu")

'''

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

prompt = "Please provide me a detailed summary of the contents of this Wikipedia page. In this summary, make sure to include the following details: 1. Name of the food\n 2. Other names for the food\n 3. Where/When/Why the food was invented\n 4. Who invented the food and how it became popular\n 5. The recipe/process to create the food\n 6. Other related foodstuffs and recipes\n Please format your short summary as multiple paragraphs instead of a bulleted or numbered list. It should flow naturally like a summary of the topic on Wikipedia."

chat_completion = client.chat.completions.create(
messages=[
    {
        "role": "user",
        "content": prompt + "Wikipedia page content: " + page.content,
    }
],
model="gpt-4",
# So I don't run out of money using GPT 4
)

gpt_summary = chat_completion.choices[0].message.content

print("Wikipedia page summarized by GPT-3.5-Turbo: \n")
print(gpt_summary + "\n")