import praw
import datetime as dt
import json
import time
import prawcore
import os

# Reddit credentials
reddit = praw.Reddit(client_id='kIl2JAx3TtA6cta50C_i4Q', 
                     client_secret='usRm7irdycBOLKi7SyARg6mUFQ8RCw', 
                     user_agent='Stelram')

subreddit = reddit.subreddit('Genshin_Impact')

def save_to_file(data, filename='genshin_impact_data.json'):
    data_directory = '../data'
    file_path = os.path.join(data_directory, filename)
    with open(file_path, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write('\n')

def process_comment(comment):
    comment_data = {
        "author": str(comment.author),
        "comment": comment.body,
        "replies": [process_comment(reply) for reply in comment.replies]
    }
    return comment_data

for submission in subreddit.hot(limit=None):
    submission.comments.replace_more(limit=None)
    comments_data = [process_comment(comment) for comment in submission.comments.list()]

    post_data = {
        "title": submission.title,
        "date": dt.datetime.fromtimestamp(submission.created_utc).isoformat(),
        "author": str(submission.author),
        "comments": comments_data
    }

    save_to_file(post_data)
    time.sleep(2)