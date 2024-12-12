import random

class TraitManager:
    def __init__(self, config):
        self.traits = config['personality']['traits']['base_traits']
        self.weights = config['personality']['traits']['trait_weights']
        self.active_traits = set()

    def get_active_traits(self):
        return self.active_traits

    def activate_random_traits(self, num_traits=2):
        self.active_traits = set(random.sample(self.traits, num_traits))

    def get_trait_influence(self):
        return {trait: self.weights[trait] for trait in self.active_traits}