from typing import Any

from pydantic import BaseModel


class FinancialsSnapshot(BaseModel):
    ticker: str
    annual_income_statement: dict[str, Any] | None = None
    quarterly_income_statement: dict[str, Any] | None = None
    annual_balance_sheet: dict[str, Any] | None = None
    quarterly_balance_sheet: dict[str, Any] | None = None
    annual_cash_flow: dict[str, Any] | None = None
    quarterly_cash_flow: dict[str, Any] | None = None
