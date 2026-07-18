import json
from typing import Any

from app.services.calendar.models import CompanyCalendar


def map_calendar(ticker: str, calendar: Any) -> CompanyCalendar:
    return CompanyCalendar(
        ticker=ticker.upper(),
        events=json.loads(json.dumps(calendar, default=str)),
    )
