from typing import Any

from pydantic import BaseModel


class HoldersSnapshot(BaseModel):
    ticker: str
    major_holders: dict[str, Any] | None = None
    institutional_holders: dict[str, Any] | None = None
    mutualfund_holders: dict[str, Any] | None = None
    insider_transactions: dict[str, Any] | None = None
    insider_purchases: dict[str, Any] | None = None
    insider_roster_holders: dict[str, Any] | None = None
