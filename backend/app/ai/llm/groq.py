from app.ai.llm.base import BaseLLM
from app.ai.llm.models import LLMRequest
from app.core.config import settings


class GroqLLM(BaseLLM):
    """Groq implementation of the application's LLM interface."""

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY must be set when LLM_PROVIDER is 'groq'.")

        try:
            from groq import Groq
        except ImportError as error:
            raise ImportError(
                "The Groq SDK is required. Install it with: pip install groq"
            ) from error

        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate(self, request: LLMRequest):
        request_options = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            "temperature": request.temperature,
        }

        if request.response_model:
            request_options["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**request_options)
        content = response.choices[0].message.content

        if content is None:
            raise ValueError("Groq returned an empty response.")

        if request.response_model:
            return request.response_model.model_validate_json(content)

        return content
