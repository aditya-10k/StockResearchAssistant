from app.ai.llm.gemini import GeminiLLM
from app.ai.llm.models import LLMRequest

class LLMService:
    def __init__(self):
        self.provider = GeminiLLM()

    def generate(self , request : LLMRequest):
        return self.provider.generate(request)

    