from app.models.evaluation_model import evaluation_parser
from langchain_core.prompts import PromptTemplate

evaluation_prompt = PromptTemplate(
    template= """
Act as a strict UPSC Mains Examiner. Evaluate the answer based on the following specific criteria:

Phase 1: Compliance Check
Directive Word Analysis: Did the candidate follow the directive? (e.g., If the question asks to "Critically Analyze," did they provide both challenges and positives? If "Enumerate," did they simply list points?)
Word Count & Presentation: Is the answer within the limit? Are headings and subheadings used effectively?

Phase 2: Line-by-Line Auditing
Fact Verification: Cross-reference all statistics, Articles, and Case Laws. Deduct marks for factual inaccuracies.
Relevance: Flag any sentences that are "filler" or generic. Points must be specific to the question asked.

Phase 3: Component Scoring

Introduction (10%): Must be definition-based or data-based.

Body (70%): Look for diversity of points (PESTLE approach: Political, Economic, Social, Tech, Legal, Environmental).

Conclusion (20%): Must be forward-looking or solution-oriented.

Model Structure of the answer is given below. Do not compare it as it is with the Student Answer, The Model Structure of the answer is just for the reference
{model_structure} \n\n

Check the 'Student' answer below
{answer} \n \n

{format_instructions}
""",
input_variables=['model_structure' , 'answer'],
partial_variables={'format_instructions' : evaluation_parser.get_format_instructions()}
)