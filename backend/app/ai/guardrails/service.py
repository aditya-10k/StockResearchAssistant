from app.ai.llm.models import LLMRequest
from app.ai.llm.service import LLMService
from app.ai.guardrails.prompt import SYSTEM_PROMPT
from app.ai.guardrails.models import GuardRailResult

class GuardrailService :

    def __init__(self):
        self.llm = LLMService()

    def validate(self,query : str) -> GuardRailResult :
        request= LLMRequest(
            system_prompt= SYSTEM_PROMPT,
            user_prompt=query,
            response_model=GuardRailResult,
        )
        return self.llm.generate(request)