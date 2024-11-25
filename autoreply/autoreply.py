import tweepy
import openai
import os
from flask import Flask, request, redirect, jsonify

# Flask app setup
app = Flask(__name__)

# Load API keys and secrets from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")  # For v2 API
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CALLBACK_URL = "https://autoreply-bot-adc8f67b7419.herokuapp.com/callback"

# Tweepy OAuth2 user handler
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=CLIENT_ID,
    redirect_uri=CALLBACK_URL,
    scope=["tweet.read", "tweet.write", "users.read"],
    client_secret=CLIENT_SECRET
)

# Corrected Tweepy client instantiation
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

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
            # Check if the tweet is from an account in ACCOUNTS_TO_REPLY
            user_id = tweet.data['author_id']
            user = client.get_user(id=user_id).data
            if user.username.lower() not in [account.lower() for account in ACCOUNTS_TO_REPLY]:
                return

            # Generate a reply using OpenAI
            prompt = f"Reply to this tweet: {tweet.data['text']}"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=50
            )
            reply_text = response.choices[0].text.strip()

            # Reply to the tweet
            reply = f"@{user.username} {reply_text}"
            client.create_tweet(
                text=reply,
                in_reply_to_tweet_id=tweet.data['id']
            )
            print(f"Replied: {reply}")

        except tweepy.TweepyException as e:
            print(f"Tweepy Error: {e}")
        except Exception as e:
            print(f"General Error: {e}")

    def on_error(self, status_code):
        print(f"Stream encountered an error: {status_code}")
        return True  # Keep the stream running


@app.route("/")
def home():
    """Home route."""
    return "AutoReply Bot is running!"

@app.route("/login")
def login():
    """Redirect to Twitter login."""
    authorization_url = oauth2_user_handler.get_authorization_url()
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    """Handle OAuth callback."""
    code = request.args.get("code")
    state = request.args.get("state")
    try:
        oauth2_user_handler.fetch_token(code=code)
        access_token = oauth2_user_handler.access_token
        refresh_token = oauth2_user_handler.refresh_token
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    except Exception as e:
        return f"Error during callback: {str(e)}", 400


def start_bot():
    """Start the stream."""
    stream = MyStream(bearer_token=BEARER_TOKEN)
    try:
        # Clear existing rules to prevent conflicts
        existing_rules = stream.get_rules().data
        if existing_rules:
            rule_ids = [rule.id for rule in existing_rules]
            stream.delete_rules(rule_ids)

        # Add rules for filtering specific accounts
        for account in ACCOUNTS_TO_REPLY:
            try:
                rule = tweepy.StreamRule(f"from:{account}")
                stream.add_rules(rule)
                print(f"Rule added: {rule.value}")
            except tweepy.TweepyException as e:
                print(f"Error adding rule for from:{account}: {e}")

        # Start filtering
        stream.filter(expansions="author_id", threaded=True)
    except tweepy.TweepyException as e:
        print(f"Stream Error: {e}")
    except Exception as e:
        print(f"General Stream Error: {e}")


if __name__ == "__main__":
    # Run Flask server for OAuth2
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
