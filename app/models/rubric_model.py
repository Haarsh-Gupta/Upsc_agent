from pydantic import BaseModel, Field
from typing import Dict, List
from langchain_core.output_parsers import JsonOutputParser

# keypoints structure
class Introduction(BaseModel):
    marks: float
    criteria: str

class Dimension(BaseModel):
    title: str
    marks: float
    expected_elements: List[str]

class Body(BaseModel):
    marks: float
    dimensions: List[Dimension]

class Conclusion(BaseModel):
    marks: int 
    criteria: str

class GradingRubric(BaseModel):
    introduction: Introduction
    body: Body
    conclusion: Conclusion

# Root Model
class EvaluationStructure(BaseModel):
    question_text: str
    max_marks: float
    grading_rubric: GradingRubric


rubric_parser = JsonOutputParser(pydantic_object= EvaluationStructure)