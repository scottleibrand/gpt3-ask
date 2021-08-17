#!/usr/bin/env python
"""
Read the GPT_API_KEY from its environment variable.
Read the question from the first argument.
Use the https://api.openai.com/v1/engines/davinci-codex/completions API to make an initial guess.
Print out that guess.
"""

#!/usr/bin/env python
import requests
import json
import sys
import os

# Set the environment variable GPT_API_KEY to your API key
GPT_API_KEY = os.environ['GPT_API_KEY']

def get_gpt_guess(question):
    prompt = "Q: {}\nA:".format(question)
    data = json.dumps({
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7,
        "stop": "Q:"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(GPT_API_KEY)
    }
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, data=data)
    return response.json()['choices'][0]['text']


"""
Read the GPT_API_KEY from its environment variable.
Read the question from the first argument.
Use the https://api.openai.com/v1/engines/davinci-codex/completions API to make an initial guess.
URL-encode the question and use python's URL libraries to search Google for the question.
In the case of an error, print out the request URL.
Retrieve the contents of the first result url.
Use https://github.com/buriy/python-readability to extract the main article text
Provide the article text to the OpenAI API, followed by the following prompt:
Q: According to the article above, $question
A:
to get OpenAI to answer the question by summarizing the article.
Print out that answer.
"""

#!/usr/bin/env python
import requests
import json
import sys
import os
import urllib.parse
import readability
from bs4 import BeautifulSoup

# Set the environment variable GPT_API_KEY to your API key
GPT_API_KEY = os.environ['GPT_API_KEY']

def get_gpt_answer(question):
    prompt = "Q: According to the article above, {}\nA:".format(question)
    data = json.dumps({
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7,
        "stop": "Q:"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(GPT_API_KEY)
    }
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, data=data)
    return response.json()['choices'][0]['text']

def get_google_answer(question):
    url = "https://www.google.com/search?q={}".format(urllib.parse.quote_plus(question))
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: {}".format(response.status_code))
        print("URL: {}".format(url))
        return None
    doc = readability.Document(response.text)
    return doc.summary()

if __name__ == '__main__':
    question = sys.argv[1]
    print("Initial guess:")
    print("Q: {}".format(question))
    print("A: {}".format(get_gpt_guess(question)))
    print("")
    print("Google search:")
    answer = get_google_answer(question)
    if answer is not None:
        print("Q: {}".format(question))
        print("A: {}".format(answer))
        print("")
        print("OpenAI answer:")
        print("Q: According to the article above, {}".format(question))
        print("A: {}".format(get_gpt_answer(answer)))
    else:
        print("No Google search results found")

