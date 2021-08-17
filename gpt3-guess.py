#!/usr/bin/env python
import requests
import json
import sys
import os

# Set the environment variable GPT_API_KEY to your API key
GPT_API_KEY = os.environ['GPT_API_KEY']

def get_gpt_answer(question):
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

if __name__ == '__main__':
    question = sys.argv[1]
    print("Initial guess:")
    print("Q: {}".format(question))
    print("A: {}".format(get_gpt_answer(question)))

