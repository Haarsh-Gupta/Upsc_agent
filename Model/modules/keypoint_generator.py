from langchain.chat_models import ChatOpenAI
from prompts.keypoints_prompt import KEYPOINTS_PROMPT
from config import LLM_MODEL, TEMP

llm = ChatOpenAI(model_name=LLM_MODEL, temperature=TEMP)

def generate_keypoints(text):
    prompt = KEYPOINTS_PROMPT.format(essay_text=text)
    return llm.predict(prompt).splitlines()
