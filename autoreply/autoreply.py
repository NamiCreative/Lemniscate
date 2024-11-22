import tweepy
import openai
import os

# Load API keys from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # Required for StreamingClient

# Authenticate with OpenAI
openai.api_key = OPENAI_API_KEY

# Specify accounts to reply to
ACCOUNTS_TO_REPLY = [
    "RaminNasibov",
    "sama",
    "0xzerebro",
    "liminal_bardo",
    "anthrupad",
    "TheMysteryDrop",
    "repligate",
    "truth_terminal",
    "QiaochuYuan",
    "AndyAyrey",
    "notthreadguy",
    "jyu_eth",
    "OpenAI",
    "eigenrobot",
    "elder_plinius",
    "deepfates",
    "pmarca"
]

# Define custom stream listener using StreamingClient
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            # Avoid processing retweets
            if tweet.referenced_tweets and any(t.ref_type == "retweeted" for t in tweet.referenced_tweets):
                return
            
            # Extract the username and tweet text
            user_id = tweet.author_id
            user = api.get_user(user_id=user_id)
            username = user.screen_name

            # Check if the tweet is from an account in ACCOUNTS_TO_REPLY
            if username.lower() not in [account.lower() for account in ACCOUNTS_TO_REPLY]:
                return

            # Generate a reply using OpenAI
            prompt = f"Reply to this tweet: {tweet.text}"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50
            )
            reply_text = response.choices[0].text.strip()

            # Reply to the tweet
            reply = f"@{username} {reply_text}"
            api.update_status(status=reply, in_reply_to_status_id=tweet.id)
            print(f"Replied to @{username}: {reply}")
        except Exception as e:
            print(f"Error: {e}")

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        if status_code == 420:  # Rate limit exceeded
            return False

# Start listening for tweets
def start_bot():
    # Initialize Twitter API for posting replies
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    global api
    api = tweepy.API(auth)

    # Initialize the stream
    stream = MyStream(BEARER_TOKEN)

    # Add rules for the accounts you want to track
    account_rules = [f"from:{account}" for account in ACCOUNTS_TO_REPLY]
    for rule in account_rules:
        try:
            stream.add_rules(tweepy.StreamRule(rule))
        except Exception as e:
            print(f"Error adding rule for {rule}: {e}")

    # Start the stream
    stream.filter(tweet_fields=["author_id", "text"], threaded=True)

if __name__ == "__main__":
    start_bot()
