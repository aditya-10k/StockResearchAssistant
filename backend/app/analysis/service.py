from app.analysis.models import AnalysisResult
from app.analysis.prompt import ANALYSIS_SYSTEM_PROMPT
from app.analysis.analysis_prompt import build_analysis_prompt

from app.ai.llm.models import LLMRequest
from app.ai.llm.service import LLMService

from app.schemas.execution_plan import ExecutionPlan
from app.services.market.models import CompanySnapshot


class AnalysisService:

    def __init__(self):

        self.llm = LLMService()

    def analyze(
        self,
        query: str,
        execution_plan: ExecutionPlan,
        market_data: list[CompanySnapshot],
        news_data : dict[str , list[dict[str,any]]],
    ) -> AnalysisResult:

        prompt = build_analysis_prompt(
            query,
            market_data,
            news_data
        )

        request = LLMRequest(
            system_prompt=ANALYSIS_SYSTEM_PROMPT,
            user_prompt=prompt,
            response_model=AnalysisResult,
        )

        return self.llm.generate(request)