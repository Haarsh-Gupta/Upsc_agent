from functools import lru_cache
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

class AIModels:
    def __init__(self):
        # We use PRO for everything except OCR to ensure JSON reliability
        # Make sure your API key is in .env
        self.flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.pro = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2)

# THIS IS THE FUNCTION YOUR ERROR SAYS IS MISSING
@lru_cache()
def get_ai_models() -> AIModels:
    return AIModels()