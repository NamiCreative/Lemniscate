class PersonalityManager:
    def __init__(self):
        self.current_mood = "neutral"
        self.moods = ["playful", "serious", "curious", "excited"]

    def update_mood(self, engagement_metrics=None):
        current_index = self.moods.index(self.current_mood)
        self.current_mood = self.moods[(current_index + 1) % len(self.moods)]
