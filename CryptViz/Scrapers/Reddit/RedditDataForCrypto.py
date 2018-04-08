import praw
import json
from datetime import datetime

reddit = praw.Reddit(
    client_id='U36iaoV0DIIQkw', 
    client_secret="-m3cdaWujHlkgb6I36xfj3wkjIM",
    user_agent='Project CryptViz'
    # Read-Only Mode
    # username='USERNAME',
    # password='PASSWORD' 
)

subreddit = reddit.subreddit('bitcoin')
#for submission in subreddit.stream.submissions():
for submission in subreddit.hot(limit=1):
    if not submission.stickied:
        print(submission.title)
        print(datetime.utcfromtimestamp(submission.created_utc))
        print(datetime.fromtimestamp(submission.created))
        #print(len(submission.comments))
        print(submission.downs)
        print(submission.ups)

#print(dir(submission))
#help(submission)