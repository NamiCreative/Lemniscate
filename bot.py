import tweepy
import random
import os

# Fetch API keys and tokens from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

# Initialize the Twitter client using Tweepy
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret
)

# List of tweets to randomly choose from
tweets = [
    ">Example Tweet 1",
    ">Example Tweet 2",
    ">Example Tweet 3"
]

# Function to post a tweet
def post_tweet(client, tweet_text):
    try:
        # Attempt to post the tweet
        client.create_tweet(text=tweet_text)
        print(f"Tweeted: {tweet_text}")
    except tweepy.TweepyException as e:
        # Print error details if the tweet fails
        print(f"An error occurred: {e}")

# Select a random tweet from the list
tweet_text = random.choice(tweets)

# Post the selected tweet
post_tweet(client, tweet_text)
