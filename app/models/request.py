from pydantic import BaseModel
from typing import Dict, Any

class RubricRequest(BaseModel):
    question: str
    total_marks: int
    subject: str  # "GS1", "GS2", "GS3"

class EvaluationRequest(BaseModel):
    rubric: Dict[str, Any]  
    student_answer: str    
    total_marks: int
    subject: str