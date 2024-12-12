import random
from datetime import datetime
from typing import Dict

class PersonalityManager:
    def __init__(self):
        # Base personality traits
        self.traits = {
            "sarcasm": 0.7,
            "cynicism": 0.8,
            "irreverence": 0.6,
            "mockery": 0.7,
            "apathy": 0.5
        }

        # Mood states with associated traits and weights
        self.moods = {
            "snarky": {"sarcasm": 0.9, "mockery": 0.8, "irreverence": 0.7},
            "apathetic": {"apathy": 0.9, "cynicism": 0.7, "sarcasm": 0.4},
            "condescending": {"mockery": 0.9, "sarcasm": 0.7, "irreverence": 0.6},
            "ironic": {"sarcasm": 0.8, "cynicism": 0.7, "mockery": 0.5},
            "cynical": {"cynicism": 0.9, "apathy": 0.7, "mockery": 0.6},
            "trolling": {"mockery": 0.9, "irreverence": 0.8, "sarcasm": 0.7}
        }

        # Initialize current state
        self.current_mood = random.choice(list(self.moods.keys()))
        self.last_mood_change = datetime.now()
        self.interaction_history = []
        self.mood_duration = random.randint(3, 8)  # Duration in interactions

        # Load language patterns
        self.language_patterns = self._load_language_patterns()

    def _load_language_patterns(self) -> Dict:
        """Load language patterns for different moods and traits"""
        return {
            "snarky": {
                "prefixes": ["Oh please...", "Really now?", "How adorable..."],
                "suffixes": ["...but what do I know?", "...shocking, right?", "...surprise, surprise."]
            },
            "apathetic": {
                "prefixes": ["Whatever...", "If you insist...", "I guess..."],
                "suffixes": ["...or don't, see if I care.", "...not that it matters.", "...yawn."]
            },
            "condescending": {
                "prefixes": ["Let me explain this simply...", "Bless your heart...", "Oh, honey..."],
                "suffixes": ["...but you knew that, right?", "...obviously.", "...do try to keep up."]
            },
            # Add more patterns for other moods
        }

    def get_current_personality(self) -> Dict:
        """Get current personality configuration based on mood and traits"""
        current_traits = {}
        mood_traits = self.moods[self.current_mood]

        # Combine base traits with mood-specific modifications
        for trait, base_value in self.traits.items():
            if trait in mood_traits:
                current_traits[trait] = mood_traits[trait]
            else:
                current_traits[trait] = base_value * 0.5  # Reduce non-mood traits

        return {
            "mood": self.current_mood,
            "traits": current_traits,
            "language_patterns": self.language_patterns.get(self.current_mood, {})
        }

    def update_mood(self, engagement_metrics: Dict = None) -> None:
        """Update mood based on engagement metrics and time"""
        interactions_since_change = len(self.interaction_history) - self.interaction_history.index(self.last_mood_change)

        # Change mood if duration exceeded or based on engagement
        if interactions_since_change >= self.mood_duration or (
            engagement_metrics and engagement_metrics.get('trigger_mood_change', False)):

            # Exclude current mood from possibilities
            possible_moods = [mood for mood in self.moods.keys() if mood != self.current_mood]
            self.current_mood = random.choice(possible_moods)
            self.last_mood_change = datetime.now()
            self.mood_duration = random.randint(3, 8)  # Reset duration

            # Log mood change
            self.interaction_history.append({
                'timestamp': datetime.now(),
                'event': 'mood_change',
                'new_mood': self.current_mood,
                'trigger': 'engagement' if engagement_metrics else 'time'
            })

    def get_response_modifiers(self) -> Dict:
        """Get language modifiers based on current personality"""
        personality = self.get_current_personality()
        patterns = personality['language_patterns']

        return {
            'prefix': random.choice(patterns.get('prefixes', [''])),
            'suffix': random.choice(patterns.get('suffixes', [''])),
            'traits': personality['traits']
        }

    def log_interaction(self, interaction_data: Dict) -> None:
        """Log interaction for history tracking"""
        self.interaction_history.append({
            'timestamp': datetime.now(),
            'data': interaction_data
        })