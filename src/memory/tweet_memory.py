class TweetMemory:
    def __init__(self, max_memory=100):
        self.tweets = []
        self.max_memory = max_memory

    def add_tweet(self, tweet):
        if len(self.tweets) >= self.max_memory:
            self.tweets.pop(0)
        self.tweets.append(tweet)

    def check_similarity(self, new_tweet):
        return any(tweet.lower() == new_tweet.lower() for tweet in self.tweets)
