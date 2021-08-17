#!/usr/bin/env bash
echo $1 > question.txt
question=$(echo $1 | sed 's/ /+/g')
lengtharg=$2
length="${lengtharg:-6000}"
#resultsarg=$3
#results="${resultsarg:-1}"
#echo $lengtharg $length $resultsarg $results

prompt=$( echo "Q: $1"
    echo -n "A:" )
data=$(echo -n "$prompt" | jq -R -s ". | {prompt: ., max_tokens: 150, temperature: 0.7, stop: \"Q:\"}")
guess=$(curl -s https://api.openai.com/v1/engines/davinci-codex/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $GPT_API_KEY" \
-d "$data")
echo $guess > guess.json
echo "Initial guess:"
echo "Q: $1"
echo -n "A:"
cat guess.json | jq ".choices[].text" | perl -p00e "s/\\\n/\n/g" | sed 's/"//g'
searchurl="https://www.google.com/search?rls=en&q=$question"
lynx -dump $searchurl | tee searchresults.txt | grep -v quora | grep "google.com/url" | head -1 | awk '{print $2}' | while read url; do
    echo Found result URL $url
    prompt=$( readable -l force --properties text-content $url | sed 's/"//g' 2>/dev/null | head -c $length | tee article.txt
        echo
        echo "Q: According to the article above, $1"
        echo -n "A:" )
    echo -n $prompt > prompt.txt
    data=$(echo -n "$prompt" | jq -R -s ". | {prompt: ., max_tokens: 150, temperature: 0.7, stop: \"Q:\"}")
    # echo $data
    echo Summarizing first $length characters...
    summary=$(curl -s https://api.openai.com/v1/engines/davinci/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $GPT_API_KEY" \
    -d "$data")
    echo $summary > summary.json
done
echo "Based on the first Google result:"
echo "Q: $1"
echo -n "A:"
cat summary.json | jq ".choices[].text" | perl -p00e "s/\\\n/\n/g" | sed 's/"//g'
grep error summary.json && cat summary.json | jq .
