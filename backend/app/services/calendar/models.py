from typing import Any

from pydantic import BaseModel


class CompanyCalendar(BaseModel):
    ticker: str
    events: Any = None
