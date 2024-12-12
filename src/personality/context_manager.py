from datetime import datetime, timedelta

class ContextManager:
    def __init__(self):
        self.interaction_history = []
        self.current_context = {}

    def add_interaction(self, tweet):
        self.interaction_history.append({
            'tweet': tweet,
            'timestamp': datetime.now()
        })

    def clean_old_interactions(self, days=7):
        cutoff = datetime.now() - timedelta(days=days)
        self.interaction_history = [
            i for i in self.interaction_history 
            if i['timestamp'] > cutoff
        ]

    def get_context(self):
        return {
            'recent_interactions': self.interaction_history[-5:],
            'current_context': self.current_context
        }