import requests

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

search = input("Please input a topic you wish to learn more about:\n")

SEARCHPAGE = search

PARAMS = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": SEARCHPAGE
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

for i in range(11):
    print(DATA['query']['search'][i]['title'])

