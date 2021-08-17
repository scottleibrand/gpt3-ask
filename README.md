# gpt3-ask
Ask GPT-3 a question, and it answers based on summary of first Google result

Requires an OpenAI GPT-3 API key.

Prerequisite:
```
npm install -g readability-cli
```

Usage:

```
export GPT_API_KEY=<your key>
gpt3-ask.sh "Why is the sky blue?"
```

If the first Google result is too complex, 6000 characters will overrun GPT-3's 2000-token context window. To work around that, you can lower the character limit, like:
  
```
gpt3-ask.sh "Why is the sky blue?" 4000
```
