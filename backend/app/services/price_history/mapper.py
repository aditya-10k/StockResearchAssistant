import json

from pandas import DataFrame

from app.services.price_history.models import PriceHistory


def map_price_history(ticker: str, history: DataFrame) -> PriceHistory:
    return PriceHistory(
        ticker=ticker.upper(),
        prices=json.loads(history.to_json(orient="split", date_format="iso")),
    )
