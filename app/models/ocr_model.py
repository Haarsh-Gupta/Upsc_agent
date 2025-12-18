from pydantic import BaseModel, Field
from typing import Dict, List
from langchain_core.output_parsers import JsonOutputParser

class Ocr(BaseModel):
    question: str = Field(description="The question asked in the exam paper.")
    answer: str = Field(description="The student's answer text.")

ocr_parser = JsonOutputParser(pydantic_object= Ocr)