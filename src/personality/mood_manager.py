import random
from datetime import datetime

class MoodManager:
    def __init__(self, config):
        self.moods = config['personality']['moods']['available_moods']
        self.current_mood = config['personality']['moods']['default']
        self.transition_prob = config['personality']['moods']['transition_probability']
        self.last_change = datetime.now()

    def get_current_mood(self):
        return self.current_mood

    def update_mood(self, engagement_metrics=None):
        if random.random() < self.transition_prob:
            self.current_mood = random.choice([m for m in self.moods if m != self.current_mood])
            self.last_change = datetime.now()