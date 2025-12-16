from .base_rubric import BaseRubric

class GSRubricGS2(BaseRubric):
    def __init__(self):
        self.weights = {
            "essential_points": 3,
            "grammar": 2,
            "jargon": 1,
            "tone_coherence": 2,
            "policy_or_ethics": 2
        }
