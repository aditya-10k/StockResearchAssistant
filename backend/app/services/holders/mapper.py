import json

from pandas import DataFrame

from app.services.holders.models import HoldersSnapshot


def _serialize_frame(frame: DataFrame | None) -> dict | None:
    if frame is None:
        return None
    return json.loads(frame.to_json(orient="split", date_format="iso"))


def map_holders(ticker: str, holders: dict[str, DataFrame | None]) -> HoldersSnapshot:
    return HoldersSnapshot(
        ticker=ticker.upper(),
        major_holders=_serialize_frame(holders["major_holders"]),
        institutional_holders=_serialize_frame(holders["institutional_holders"]),
        mutualfund_holders=_serialize_frame(holders["mutualfund_holders"]),
        insider_transactions=_serialize_frame(holders["insider_transactions"]),
        insider_purchases=_serialize_frame(holders["insider_purchases"]),
        insider_roster_holders=_serialize_frame(holders["insider_roster_holders"]),
    )
