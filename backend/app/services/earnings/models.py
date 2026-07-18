from typing import Any

from pydantic import BaseModel


class EarningsSnapshot(BaseModel):
    ticker: str
    earnings_dates: dict[str, Any] | None = None
    annual_earnings: dict[str, Any] | None = None
    quarterly_earnings: dict[str, Any] | None = None
