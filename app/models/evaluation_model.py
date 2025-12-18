from pydantic import BaseModel, Field
from typing import Dict, List
from langchain_core.output_parsers import JsonOutputParser


class MarksBreakdown(BaseModel):
    introduction: float = Field(alias="Introduction")
    body: float = Field(alias="Body")
    conclusion: float = Field(alias="Conclusion")
    total: float = Field(alias="Total")

class FeedbackDetail(BaseModel):
    introduction_comments: List[str] = Field(alias="Introduction")
    body_comments: List[str] = Field(alias="Body")
    conclusion_comments: List[str] = Field(alias="Conclusion")
    misc_comments: List[str] = Field(alias="Misc")
    spelling_errors: List[str] = Field(alias="Spelling errors")
    
    marks: MarksBreakdown = Field(alias="Total mark")

# Root Model
class EvaluationOutput(BaseModel):
    feedback: FeedbackDetail


evaluation_parser = JsonOutputParser(pydantic_object= EvaluationOutput)