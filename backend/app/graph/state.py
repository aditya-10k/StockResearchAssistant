from typing import TypedDict
from app.schemas.execution_plan import ExecutionPlan
from app.services.market.models import CompanySnapshot
from app.analysis.models import AnalysisResult
from app.ai.guardrails.models import GuardRailResult

class GraphState(TypedDict):
    query : str
    guardrail: GuardRailResult | None
    execution_plan : ExecutionPlan | None
    market_data : list[CompanySnapshot] | None
    news_data : dict[str , list] | None
    analysis : AnalysisResult | None
