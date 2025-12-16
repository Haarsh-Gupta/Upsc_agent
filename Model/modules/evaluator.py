from langchain.chat_models import ChatOpenAI
from prompts.evaluation_prompt import EVALUATION_PROMPT
from config import LLM_MODEL, TEMP
import json

llm = ChatOpenAI(model_name=LLM_MODEL, temperature=TEMP)

def evaluate_essay(essay, context):
    ctx = "\n\n".join([d.page_content for d in context]) if context else ""
    prompt = EVALUATION_PROMPT.format(essay=essay, context=ctx)
    raw = llm.predict(prompt)

    try:
        return json.loads(raw)
    except:
        return {"comments": raw}
