from .base_rubric import BaseRubric

class GSRubricGS3(BaseRubric):
    def __init__(self):
        self.weights = {
            "essential_points": 3,
            "grammar": 1.5,
            "jargon": 2.5,
            "tone_coherence": 1.5,
            "policy_or_ethics": 1.5
        }
