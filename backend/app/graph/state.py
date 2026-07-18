from typing import TypedDict
from app.schemas.execution_plan import ExecutionPlan
from app.services.market.models import CompanySnapshot
from app.services.financials.models import FinancialsSnapshot
from app.services.price_history.models import PriceHistory
from app.services.calendar.models import CompanyCalendar
from app.services.holders.models import HoldersSnapshot
from app.services.recommendations.models import RecommendationsSnapshot
from app.services.earnings.models import EarningsSnapshot
from app.analysis.models import AnalysisResult
from app.ai.guardrails.models import GuardRailResult

class GraphState(TypedDict):
    query : str
    guardrail: GuardRailResult | None
    execution_plan : ExecutionPlan | None
    market_data : list[CompanySnapshot] | None
    news_data : dict[str , list] | None
    financials_data: dict[str, FinancialsSnapshot] | None
    price_history_data: dict[str, PriceHistory] | None
    calendar_data: dict[str, CompanyCalendar] | None
    holders_data: dict[str, HoldersSnapshot] | None
    recommendations_data: dict[str, RecommendationsSnapshot] | None
    earnings_data: dict[str, EarningsSnapshot] | None
    analysis : AnalysisResult | None
