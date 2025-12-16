from .base_rubric import BaseRubric

class GSRubricGS4(BaseRubric):
    def __init__(self):
        self.weights = {
            "essential_points": 3,
            "grammar": 2,
            "jargon": 0.5,
            "tone_coherence": 3,
            "policy_or_ethics": 1.5
        }
