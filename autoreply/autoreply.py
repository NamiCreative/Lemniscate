import tweepy
import openai
import os

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
    "pmarca"
]

# Listener for replies
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # Avoid replying to your own tweets
        if status.user.screen_name.lower() == api.me().screen_name.lower():
            return
        
        # Check if the tweet is from an account in ACCOUNTS_TO_REPLY
        if status.user.screen_name.lower() not in [account.lower() for account in ACCOUNTS_TO_REPLY]:
            return

        # Generate a reply using OpenAI
        try:
            prompt = f"Reply to this tweet: {status.text}"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50
            )
            reply_text = response.choices[0].text.strip()

            # Reply to the tweet
            reply = f"@{status.user.screen_name} {reply_text}"
            api.update_status(reply, in_reply_to_status_id=status.id)
            print(f"Replied: {reply}")
        except Exception as e:
            print(f"Error: {e}")

# Start listening for tweets
def start_bot():
    stream_listener = MyStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=["keyword1", "keyword2"], is_async=True)  # Add your keywords here

if __name__ == "__main__":
    start_bot()
