from .gs1 import GSRubricGS1
from .gs2 import GSRubricGS2
from .gs3 import GSRubricGS3
from .gs4 import GSRubricGS4

def get_rubric(paper):
    p = paper.lower()

    if p == "gs1": return GSRubricGS1()
    if p == "gs2": return GSRubricGS2()
    if p == "gs3": return GSRubricGS3()
    if p == "gs4": return GSRubricGS4()

    raise ValueError("Invalid GS Paper")
