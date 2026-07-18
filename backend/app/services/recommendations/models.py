from typing import Any

from pydantic import BaseModel


class RecommendationsSnapshot(BaseModel):
    ticker: str
    recommendations: dict[str, Any] | None = None
    recommendations_summary: dict[str, Any] | None = None
    upgrades_downgrades: dict[str, Any] | None = None
