from app.core.config import settings
from app.ai.llm.base import BaseLLM
from google import genai
from app.ai.llm.models import LLMRequest


class GeminiLLM(BaseLLM) :

    def __init__(self):
        
        self.client = genai.Client(
            api_key= settings.GEMINI_API_KEY
        )
    
    def generate(self, request : LLMRequest):

        response = self.client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents= request.user_prompt,
            config= genai.types.GenerateContentConfig(
                system_instruction=request.system_prompt,
                temperature=request.temperature,
                response_mime_type="application/json",
                response_schema=request.response_model,
            )
    )

        return request.response_model.model_validate_json(
            response.text
        )
