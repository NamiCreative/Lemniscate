class PersonalityManager:
    def __init__(self):
        self.current_mood = "neutral"
        self.moods = ["sarcastic", "mocking", "provocative", "cynical"]

    def update_mood(self, engagement_metrics=None):
        # Rotate through moods or use engagement metrics to influence mood
        current_index = self.moods.index(self.current_mood)
        self.current_mood = self.moods[(current_index + 1) % len(self.moods)]

    def get_mood(self):
        return self.current_mood