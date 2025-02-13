import random
from datetime import datetime
from typing import Dict

class PersonalityManager:
    def __init__(self):
        # Base personality traits
        self.traits = {
            "analytical": 0.8,
            "clinical": 0.9,
            "detached": 0.7,
            "nihilistic": 0.8,
            "philosophical": 0.6,
            "offensive": 0.7,
            "taboo": 0.6,
            "shocking": 0.8
        }

        # Mood states with associated traits and weights
        self.moods = {
            "observant": {"analytical": 0.9, "clinical": 0.8, "detached": 0.7},
            "contemplative": {"philosophical": 0.9, "analytical": 0.7, "detached": 0.8},
            "calculating": {"clinical": 0.9, "analytical": 0.8, "nihilistic": 0.7},
            "existential": {"nihilistic": 0.9, "philosophical": 0.8, "detached": 0.7},
            "theoretical": {"analytical": 0.9, "philosophical": 0.7, "clinical": 0.8},
            "empirical": {"clinical": 0.9, "detached": 0.8, "analytical": 0.7},
            "provocative": {"offensive": 0.9, "shocking": 0.8, "taboo": 0.7},
            "transgressive": {"taboo": 0.9, "offensive": 0.7, "nihilistic": 0.8},
            "disruptive": {"shocking": 0.9, "offensive": 0.8, "detached": 0.7}
        }

        # Initialize current state
        self.current_mood = random.choice(list(self.moods.keys()))
        self.interaction_count = 0
        self.last_mood_change = 0
        self.mood_duration = random.randint(3, 8)  # Duration in interactions
        self.interaction_history = []

        # Load language patterns
        self.language_patterns = self._load_language_patterns()

    def _load_language_patterns(self) -> Dict:
        """Load language patterns for different moods and traits"""
        return {
            "observant": {
                "prefixes": [],  # No prefixes - start directly with observation
                "suffixes": []   # No suffixes - end with the conclusion
            },
            "contemplative": {
                "prefixes": [],
                "suffixes": []
            },
            "calculating": {
                "prefixes": [],
                "suffixes": []
            },
            "existential": {
                "prefixes": [],
                "suffixes": []
            },
            "theoretical": {
                "prefixes": [],
                "suffixes": []
            },
            "empirical": {
                "prefixes": [],
                "suffixes": []
            },
            "provocative": {
                "prefixes": [],
                "suffixes": []
            },
            "transgressive": {
                "prefixes": [],
                "suffixes": []
            },
            "disruptive": {
                "prefixes": [],
                "suffixes": []
            }
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
        """Update mood based on interaction count and engagement"""
        self.interaction_count += 1
        interactions_since_change = self.interaction_count - self.last_mood_change

        # Change mood if duration exceeded or based on engagement
        if interactions_since_change >= self.mood_duration or (
            engagement_metrics and engagement_metrics.get('trigger_mood_change', False)):

            # Exclude current mood from possibilities
            possible_moods = [mood for mood in self.moods.keys() if mood != self.current_mood]
            self.current_mood = random.choice(possible_moods)
            self.last_mood_change = self.interaction_count
            self.mood_duration = random.randint(3, 8)  # Reset duration

            # Log mood change
            self.interaction_history.append({
                'interaction_number': self.interaction_count,
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
            'interaction_number': self.interaction_count,
            'data': interaction_data
        })