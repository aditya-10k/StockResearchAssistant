from app.ai.llm.gemini import GeminiLLM
from app.ai.llm.groq import GroqLLM
from app.ai.llm.models import LLMRequest
from app.core.config import settings

class LLMService:
    def __init__(self):
        if settings.LLM_PROVIDER == "groq":
            self.provider = GroqLLM()
        else:
            self.provider = GeminiLLM()

    def generate(self , request : LLMRequest):
        return self.provider.generate(request)

    
