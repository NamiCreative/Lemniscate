import time
import tweepy
import random

# API keys and tokens
api_key = "zq7MGygPxEphWYQsSKfk6XuXY"
api_secret = "PSi4lwxuWzw00xJkQJgSphtvImNqo7SX5jDNVjD6apK5Ae3vTq"
access_token = "1859184398890926081-JLZz0hcxR6F8wvQ9KXI854G6mGP4fk"
access_secret = "d8w4EDPwmxbz0Jz4YqR94s6DpyWRBWOdMokOG0EeL4gPX"
bearer_token = "AAAAAAAAAAAAAAAAAAAAABNSxAEAAAAApnnKnRjv%2BI7HGadsU9Ajxq7D7Wg%3DUG7lG1RyeDL9rOT4WEmRozyQU0wIf4uSUMhvPpLzlKyMrMaXfh"

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
