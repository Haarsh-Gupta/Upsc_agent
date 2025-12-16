EVALUATION_PROMPT = """
Evaluate the essay using a strict rubric.

Essay:
{essay}

Context:
{context}

Return JSON with keys:
grammar, coherence, relevance, factuality, tone, comments.
"""
