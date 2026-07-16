from typing import Type
from pydantic import BaseModel

class LLMRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    temperature: float = 0.2
    response_model: Type[BaseModel] | None = None
    