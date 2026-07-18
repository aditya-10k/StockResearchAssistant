from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class Intent(str , Enum):
    COMPANY_ANALYSIS = "company_analysis"
    COMPANY_COMPARISON = "company_comparison"
    PORTFOLIO_ANALYSIS = "portfolio_analysis"
    GENERAL_FINANCE = "general_finance"


class Company(BaseModel):
    company : str
    ticker: str = Field(
        description="A Yahoo Finance ticker, including an exchange suffix when required "
        "(for example, PAYTM.NS and RVNL.NS for NSE-listed Indian equities)."
    )

class ServiceType(str , Enum) :
    MARKET = "market_data"
    NEWS = "news_sentiment"
    FINANCIALS = "financials"
    PRICE_HISTORY = "price_history"
    CALENDAR = "calendar"
    HOLDERS = "holders"
    RECOMMENDATIONS = "recommendations"
    EARNINGS = "earnings"
    KNOWLEDGE = "knowledge_base"
    PORTFOLIO = "portfolio"   

class ExecutionPlan(BaseModel):
    intent : Intent
    entities : List[Company]
    required_services : List[ServiceType]
