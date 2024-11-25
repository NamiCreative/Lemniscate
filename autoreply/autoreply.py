import tweepy
import openai
import os

# Triggering new build on Heroku


# Load API keys from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Authenticate with Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

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
    "pmarca",
]

# Listener for replies
class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            # Avoid replying to your own tweets
            if tweet.author_id == api.me().id_str:
                return

            # Check if the tweet is from an account in ACCOUNTS_TO_REPLY
            user = api.get_user(user_id=tweet.author_id)
            if user.screen_name.lower() not in [account.lower() for account in ACCOUNTS_TO_REPLY]:
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
            reply = f"@{user.screen_name} {reply_text}"
            api.update_status(reply, in_reply_to_status_id=tweet.id)
            print(f"Replied: {reply}")

        except tweepy.errors.TweepyException as e:
            print(f"Tweepy Error: {e}")
        except Exception as e:
            print(f"General Error: {e}")

# Start listening for tweets
def start_bot():
    stream = MyStream(bearer_token=API_KEY)
    try:
        # Add rules for filtering specific accounts
        for account in ACCOUNTS_TO_REPLY:
            try:
                stream.add_rules(tweepy.StreamRule(f"from:{account}"))
            except tweepy.errors.TweepyException as e:
                print(f"Error adding rule for from:{account}: {e}")
        
        stream.filter(expansions="author_id", threaded=True)
    except tweepy.errors.TweepyException as e:
        print(f"Stream Error: {e}")
    except Exception as e:
        print(f"General Stream Error: {e}")

if __name__ == "__main__":
    start_bot()
