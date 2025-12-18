from app.models.ocr_model import ocr_parser
from langchain_core.prompts import PromptTemplate

# Ocr Prompt
ocr_prompt = PromptTemplate(
    template= """
Role: You are a highly precise Optical Character Recognition (OCR) expert specializing in messy or cursive handwritten academic documents.
Task: Analyze the provided image of a student's essay and extract the content according to these strict rules:

1. The Question: Identify the specific question or prompt the student is answering. If it is not explicitly written, infer the most likely question based on the content of the essay.
2. The Transcription: Transcribe the body of the essay with 100% literal accuracy.
Do NOT fix spelling mistakes, punctuation, or grammatical errors.
Maintain original line breaks where possible to preserve the structure.

3. Diagrams: If you encounter a drawing, chart, or diagram, do not attempt to transcribe the text inside it. Instead, insert a placeholder: [Diagram: Provide a brief, one-sentence description of what the diagram depicts].

{format_instructions}
""",
input_variables=[],
partial_variables={"format_instructions": ocr_parser.get_format_instructions()}
)
