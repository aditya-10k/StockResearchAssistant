from enum import Enum
from typing import List
from pydantic import BaseModel

class Intent(str , Enum):
    COMPANY_ANALYSIS = "company_analysis"
    COMPANY_COMPARISON = "company_comparison"
    PORTFOLIO_ANALYSIS = "portfolio_analysis"
    GENERAL_FINANCE = "general_finance"


class Company(BaseModel):
    company : str
    ticker : str

class ExecutionPlan(BaseModel):
    intent : Intent
    entities : List[Company]
    required_services : List[str]

