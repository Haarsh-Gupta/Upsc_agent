from langchain.chat_models import ChatOpenAI
from prompts.essay_prompt import ESSAY_PROMPT
from config import LLM_MODEL, TEMP

llm = ChatOpenAI(model_name=LLM_MODEL, temperature=TEMP)

def generate_essay(title, keypoints, context_docs):
    context_text = "\n\n".join([d.page_content for d in context_docs])
    kp = "\n".join(keypoints)

    prompt = ESSAY_PROMPT.format(
        title=title,
        keypoints=kp,
        context=context_text
    )
    return llm.predict(prompt)
