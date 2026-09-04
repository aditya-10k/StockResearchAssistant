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
        import json
        system_prompt = request.system_prompt
        if request.response_model:
            schema_str = json.dumps(request.response_model.model_json_schema())
            system_prompt += f"\n\nYou MUST return a valid JSON object strictly matching this JSON Schema:\n{schema_str}"

        # Budget max_tokens per node so total query stays strictly under Groq's 1000 OTPM
        if request.response_model:
            model_name = getattr(request.response_model, "__name__", "")
            if "GuardRail" in model_name:
                max_tokens = 60
            elif "ExecutionPlan" in model_name:
                max_tokens = 180
            elif "Analysis" in model_name:
                max_tokens = 700
            else:
                max_tokens = 300
        elif "verification" in system_prompt.lower() or "compliance" in system_prompt.lower():
            max_tokens = 150
        else:
            max_tokens = 600

        request_options = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
            "temperature": request.temperature,
            "max_tokens": max_tokens,
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
