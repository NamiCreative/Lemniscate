import time
import tweepy
import random
import os

# API keys and tokens from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

# Initialize the Client
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret
)

# List of tweets without images
tweets = [
    '>Example Tweet'
]

# Function to post a tweet
def post_tweet(client, tweet_text):
    try:
        client.create_tweet(text=tweet_text)
        print(f"Tweeted: {tweet_text}")
    except tweepy.TweepyException as e:
        print(f"An error occurred: {e}")

# Loop to post tweets every hour
while True:
    tweet_text = random.choice(tweets)
    post_tweet(client, tweet_text)
    time.sleep(3600)  # Wait for one hour before posting the next tweet
