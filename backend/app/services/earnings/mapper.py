import json

from pandas import DataFrame

from app.services.earnings.models import EarningsSnapshot


def _serialize_frame(frame: DataFrame | None) -> dict | None:
    if frame is None:
        return None
    return json.loads(frame.to_json(orient="split", date_format="iso"))


def map_earnings(ticker: str, earnings: dict[str, DataFrame | None]) -> EarningsSnapshot:
    return EarningsSnapshot(
        ticker=ticker.upper(),
        earnings_dates=_serialize_frame(earnings["earnings_dates"]),
        annual_earnings=_serialize_frame(earnings["annual_earnings"]),
        quarterly_earnings=_serialize_frame(earnings["quarterly_earnings"]),
    )
