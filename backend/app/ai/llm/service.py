from app.ai.llm.gemini import GeminiLLM
from app.ai.llm.groq import GroqLLM
from app.ai.llm.models import LLMRequest
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.providers = []
        
        # Load primary provider based on settings, then fallback
        if settings.LLM_PROVIDER == "groq":
            if settings.GROQ_API_KEY:
                self.providers.append(GroqLLM())
            if settings.GEMINI_API_KEY:
                self.providers.append(GeminiLLM())
        else:
            if settings.GEMINI_API_KEY:
                self.providers.append(GeminiLLM())
            if settings.GROQ_API_KEY:
                self.providers.append(GroqLLM())

        if not self.providers:
            raise ValueError("No LLM API keys configured in environment.")

    def generate(self, request: LLMRequest):
        last_error = None
        
        for provider in self.providers:
            try:
                return provider.generate(request)
            except Exception as e:
                provider_name = provider.__class__.__name__
                print(f"[LLMService] WARNING: {provider_name} failed with error: {e}. Switching to next provider...")
                last_error = e
                continue
                
        # If all providers fail, raise the last exception
        raise last_error
