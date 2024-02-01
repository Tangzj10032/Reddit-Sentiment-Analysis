import json
import time
import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

file_path = '../data/comments_sample.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Process each comment
for comments in data:
    text=comments['comment']
    openai.api_key = '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'
    stream = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"You are a text segment robot, now please break down this Genshin Impact community comment into different parts, each part correspond to a different topic, and print the topic with the corresponding text: '{text}'"
        }], 
        stream=True,
    )
    time.sleep(2)
    

    print(f"Original Comment: {comments['comment']}\n")
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
        sentiment_score = analyzer.polarity_scores(chunk.choices[0].delta.content)
    print(f"Sentiment Score: {sentiment_score}\n")

