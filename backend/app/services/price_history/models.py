from typing import Any

from pydantic import BaseModel


class PriceHistory(BaseModel):
    ticker: str
    prices: dict[str, Any]
