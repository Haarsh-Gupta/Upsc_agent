class BaseRubric:
    weights = {}

    def compute(self, llm_scores):
        def w(key):
            return (llm_scores.get(key, 0) / 10) * self.weights[key]

        result = {
            "essential_points": round(w("essential_points"), 2),
            "grammar": round(w("grammar"), 2),
            "jargon": round(w("jargon"), 2),
            "tone_coherence": round(w("tone_coherence"), 2),
            "policy_or_ethics": round(w("policy_or_ethics"), 2),
        }
        result["total"] = round(sum(result.values()), 2)
        return result
