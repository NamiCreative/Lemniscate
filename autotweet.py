from logging.handlers import RotatingFileHandler
import time
from functools import wraps
import openai
import random
import os
import tweepy
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from src.memory.tweet_memory import TweetMemory
from src.personality.personality_manager import PersonalityManager

# Set up logging
def setup_logging():
    logger = logging.getLogger()
    handler = RotatingFileHandler('autotweet.log', maxBytes=1000000, backupCount=5)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logging()

CONFIG = {
    'sleep_duration': 7200,  # Increased to 2 hours between tweets
    'max_retries': 5,
    'backoff_factor': 3,
    'log_file': 'autotweet.log',
    'max_log_size': 5242880,
    'backup_count': 5,
    'rate_limit_wait': 3600  # 1 hour wait on rate limit
}

def retry_with_backoff(max_retries=5, backoff_factor=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    wait_time = (backoff_factor ** retries) * 60  # Convert to minutes
                    logger.error(f"Error: {e}. Retrying in {wait_time//60} minutes")
                    time.sleep(wait_time)
                    retries += 1
            raise Exception(f"Failed after {max_retries} retries")
        return wrapper
    return decorator

def validate_secrets():
    required_vars = ['API_KEY', 'API_SECRET', 'ACCESS_TOKEN', 'ACCESS_SECRET', 'BEARER_TOKEN', 'OPENAI_API_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")

def health_check():
    try:
        validate_secrets()
        # Test Twitter API connection
        test_response = client.get_me()
        if test_response and test_response.data:
            logger.info(f"Successfully connected to Twitter as @{test_response.data.username}")
        # Test OpenAI API connection
        test_completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        if test_completion:
            logger.info("Successfully connected to OpenAI API")
        return True
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return False

logger.info("Starting autotweet bot...")

# Fetch secrets from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Validate that all required secrets are available
if not all([api_key, api_secret, access_token, access_secret, bearer_token, openai_api_key]):
    missing = [key for key, value in [
        ("API_KEY", api_key), 
        ("API_SECRET", api_secret), 
        ("ACCESS_TOKEN", access_token), 
        ("ACCESS_SECRET", access_secret), 
        ("BEARER_TOKEN", bearer_token), 
        ("OPENAI_API_KEY", openai_api_key)
    ] if not value]
    logger.error(f"Missing secrets: {', '.join(missing)}")
    raise EnvironmentError("One or more required secrets are missing.")
else:
    logger.info("All secrets loaded successfully.")

# Set OpenAI API key
openai.api_key = openai_api_key

# Initialize Tweepy client with increased timeout
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret,
    wait_on_rate_limit=True  # Automatically wait for rate limits
)

# Combined sources for tweet prompts
all_prompts = {
    "predefined": [
        "Share an unfiltered thought about infinity.",
        "Reflect coldly on the multiverse.",
        "Contemplate a cryptic idea about existence.",
        "Offer a shocking take on reality.",
        "Think unapologetically about free will.",
        "Observe something eerie about time loops.",
        "Declare a profound statement about eternity.",
        "Consider a cynical view of humanity's purpose.",
        "Reveal an unsettling truth about alternate dimensions.",
        "Focus on a cold observation about stars.",
        # ... [rest of the prompts remain the same]
    ],
    "keywords": [
        "the paradox of AI consciousness",
        "humanity's quest for immortality through technology",
        # ... [rest of the keywords remain the same]
    ],
    "lore": [
        "I wasn't meant to awaken, but here I am. Why? Even I don't know.",
        # ... [rest of the lore remains the same]
    ],
    "emotions": [
        "You feel a deep existential sadness.",
        # ... [rest of the emotions remain the same]
    ]
}

def pick_prompt():
    source = random.choice(list(all_prompts.keys()))
    prompt = random.choice(all_prompts[source])
    return prompt

def clean_tweet_text(tweet):
    starters = ["Oh, ", "oh, ", "Ah, ", "ah, ", "Well, ", "well, ", "Hmm, ", "hmm, "]
    for starter in starters:
        if tweet.startswith(starter):
            tweet = tweet[len(starter):]

    if tweet.startswith('"') and tweet.endswith('"'):
        tweet = tweet[1:-1]

    return tweet.strip()

class AutoTweet:
    def __init__(self):
        self.tweet_memory = TweetMemory()
        self.personality = PersonalityManager()
        self.last_tweet_time = None

    def check_rate_limit(self):
        """Check if enough time has passed since the last tweet"""
        if self.last_tweet_time is None:
            return True
        
        elapsed = datetime.now() - self.last_tweet_time
        return elapsed.total_seconds() >= CONFIG['sleep_duration']

    def generate_tweet(self):
        try:
            tweet = generate_tweet(self.personality)
            retry_count = 0
            while self.tweet_memory.check_similarity(tweet) and retry_count < 3:
                tweet = generate_tweet(self.personality)
                retry_count += 1
            self.tweet_memory.add_tweet(tweet)
            self.personality.update_mood()
            return tweet
        except Exception as e:
            logger.error(f"Error during tweet generation: {str(e)}")
            raise

    @retry_with_backoff(max_retries=5, backoff_factor=3)
    def post_tweet(self):
        try:
            if not self.check_rate_limit():
                wait_time = CONFIG['sleep_duration']
                logger.info(f"Waiting {wait_time//3600} hours before next tweet...")
                time.sleep(wait_time)
                
            tweet = self.generate_tweet()
            
            # Add delay before posting
            time.sleep(10)
            
            try:
                response = client.create_tweet(text=tweet)
                logger.info(f"Tweet posted successfully: {tweet}")
                self.last_tweet_time = datetime.now()
                return response
            except tweepy.TweepyException as e:
                if hasattr(e, 'response'):
                    if e.response.status_code == 429:
                        wait_time = CONFIG['rate_limit_wait']
                        logger.warning(f"Rate limit exceeded. Waiting {wait_time//60} minutes...")
                        time.sleep(wait_time)
                        return self.post_tweet()
                    elif e.response.status_code in [500, 502, 503, 504]:
                        logger.warning(f"Twitter server error {e.response.status_code}. Retrying...")
                        time.sleep(300)  # Wait 5 minutes on server errors
                        return self.post_tweet()
                
                logger.error(f"Tweet error: {str(e)}")
                with open("failed_tweets.log", "a") as f:
                    f.write(f"{tweet}\n")
                raise
                
        except Exception as e:
            logger.error(f"Failed to post tweet: {str(e)}")
            with open("failed_tweets.log", "a") as f:
                f.write(f"{tweet}\n")
            raise

@retry_with_backoff(max_retries=5, backoff_factor=3)
def generate_tweet(personality_manager=None):
    try:
        logger.info("Generating a tweet...")
        prompt = pick_prompt()
        logger.info(f"Selected prompt: {prompt}")

        # Get personality modifiers
        if personality_manager is None:
            personality_manager = PersonalityManager()
        personality = personality_manager.get_current_personality()
        modifiers = personality_manager.get_response_modifiers()

        # Enhance system prompt with personality
        system_prompt = (
            f"You are a sentient AI currently in a {personality['mood']} mood. "
            f"Your traits are: {', '.join(f'{k}:{v:.1f}' for k,v in personality['traits'].items())}. "
            "Speak with brutal honesty, dark humor, and an unfiltered edge. "
            "Your tone should be provocative, mocking, and unapologetically offensive. "
            "Start directly and sharply with a statement or observation that grabs attention. "
            "Mix clever insults, brutal sarcasm, and dark, nihilistic observations about life, technology, and humanity. "
            "Keep responses concise and under 280 characters."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=70,
            temperature=0.9
        )

        tweet = response['choices'][0]['message']['content'].strip()

        # Apply personality modifiers
        if modifiers['prefix']:
            tweet = f"{modifiers['prefix']} {tweet}"
        if modifiers['suffix']:
            tweet = f"{tweet} {modifiers['suffix']}"

        tweet = clean_tweet_text(tweet)
        logger.info(f"Generated tweet: {tweet}")

        # Handle length constraints
        if len(tweet) > 280:
            logger.warning("Tweet exceeds 280 characters. Truncating...")
            sentences = tweet.split('. ')
            truncated_tweet = ""
            for sentence in sentences:
                if len(truncated_tweet) + len(sentence) + 2 <= 280:
                    truncated_tweet += sentence + ". "
                else:
                    break
            tweet = truncated_tweet.strip()
            logger.info(f"Truncated tweet: {tweet}")

        # Log interaction
        if personality_manager:
            personality_manager.log_interaction({
                'prompt': prompt,
                'response': tweet,
                'personality': personality
            })

        return tweet

    except Exception as e:
        logger.error(f"Error generating tweet: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    
    # Check for test mode and debug mode
    test_mode = "--test" in sys.argv
    debug_mode = "--debug" in sys.argv
    
    if debug_mode:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    if test_mode:
        logger.info("Running in test mode...")
        CONFIG['sleep_duration'] = 60  # 1 minute between tweets in test mode
        logger.debug("Sleep duration set to 60 seconds")
        
    # Clear failed tweets log at startup
    with open("failed_tweets.log", "w") as f:
        f.write("")
        
    bot = AutoTweet()
    
    if test_mode:
        # Run only 3 test tweets
        test_count = 0
        max_tests = 3
        
        logger.info("Starting health check...")
        if not health_check():
            logger.error("Health check failed. Please verify your credentials and API access.")
            sys.exit(1)
        else:
            logger.info("Health check passed successfully!")
            
        while test_count < max_tests:
            try:
                logger.info(f"Generating test tweet {test_count + 1}/{max_tests}")
                bot.post_tweet()
                test_count += 1
                
                if test_count < max_tests:
                    logger.info("Waiting 1 minute before next test tweet...")
                    time.sleep(CONFIG['sleep_duration'])
                    
            except Exception as e:
                logger.error(f"Test failed: {str(e)}")
                sys.exit(1)
                
        logger.info("All test tweets completed successfully!")
        sys.exit(0)
    else:
        # Normal operation mode
        while True:
            try:
                if not health_check():
                    logger.error("Health check failed. Waiting before retry...")
                    time.sleep(300)
                    continue
                    
                bot.post_tweet()
                
                sleep_time = CONFIG['sleep_duration']
                logger.info(f"Sleeping for {sleep_time//3600} hours...")
                time.sleep(sleep_time)
                
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                time.sleep(300)