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

# Retry function
def with_retry(func, *args, max_retries=5, initial_delay=60):
    retry_count = 0
    delay = initial_delay

    while retry_count < max_retries:
        try:
            return func(*args)
        except prawcore.exceptions.RequestException as e:
            print(f"RequestException: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            retry_count += 1
            delay *= 2  # Exponential backoff
        except prawcore.exceptions.ResponseException as e:
            if e.response.status_code == 429:
                print(f"Hit rate limit. Retrying in {delay} seconds...")
                time.sleep(delay)
                retry_count += 1
                delay *= 2  # Exponential backoff
            else:
                raise
        except Exception as e:
            print(f"Unhandled exception: {e}. Exiting.")
            raise
    raise Exception("Max retries reached, unable to proceed.")

for submission in subreddit.hot(limit=None):
    submission.comments.replace_more(limit=None)
    comments_data = [{"author": str(comment.author), "comment": comment.body} 
                     for comment in submission.comments.list()]

    post_data = {
        "title": submission.title,
        "date": dt.datetime.fromtimestamp(submission.created_utc).isoformat(),
        "author": str(submission.author),
        "comments": comments_data
    }

    save_to_file(post_data)
    time.sleep(2)