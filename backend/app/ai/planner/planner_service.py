from app.ai.llm.models import LLMRequest
from app.ai.llm.service import LLMService
from app.ai.planner.prompt import PLANNER_SYSTEM_PROMPT
from app.schemas.execution_plan import ExecutionPlan

class PlannerService :

    def __init__(self):
        self.llm = LLMService()

    def create_plan(self,query : str) -> ExecutionPlan :
        request= LLMRequest(
            system_prompt= PLANNER_SYSTEM_PROMPT,
            user_prompt=query,
            response_model=ExecutionPlan,
        )
        return self.llm.generate(request)

