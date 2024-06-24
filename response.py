from openai import OpenAI
import os

import wikipedia



client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Write a list of the top 5 location spots in Japan and explain why in concise detail.",
        }
    ],
    model="gpt-3.5-turbo",
    # So I don't run out of money using GPT 4
)

print("\n")

print(chat_completion)

print("\n")

response_message = chat_completion.choices[0].message.content
print(response_message)