from abc import ABC , abstractmethod
from app.ai.llm.models import LLMRequest

class BaseLLM(ABC):
    
    @abstractmethod
    def generate(self , request :LLMRequest ) -> str:
        pass