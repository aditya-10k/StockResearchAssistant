from enum import Enum
from typing import List, Any
from pydantic import BaseModel, Field, model_validator

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

    @model_validator(mode='before')
    @classmethod
    def normalize_plan(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Normalize intent
            intent = data.get('intent', '')
            if isinstance(intent, str) and intent not in [i.value for i in Intent]:
                lower_i = intent.lower()
                if any(w in lower_i for w in ['compare', 'comparison', 'vs']):
                    data['intent'] = Intent.COMPANY_COMPARISON
                elif 'portfolio' in lower_i:
                    data['intent'] = Intent.PORTFOLIO_ANALYSIS
                else:
                    data['intent'] = Intent.COMPANY_ANALYSIS
            # Normalize entities
            if 'entities' not in data and 'tickers' in data:
                tickers = data.get('tickers', [])
                companies = data.get('companies', tickers)
                entities = []
                for idx, t in enumerate(tickers):
                    c = companies[idx] if idx < len(companies) else t
                    entities.append({'company': str(c), 'ticker': str(t)})
                data['entities'] = entities
        return data

