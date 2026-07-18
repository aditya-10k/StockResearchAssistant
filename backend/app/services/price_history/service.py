from datetime import date

import yfinance as yf

from app.services.price_history.mapper import map_price_history


class PriceHistoryService:
    def get_price_history(
        self,
        ticker: str,
        period: str = "1y",
        interval: str = "1d",
        start: date | str | None = None,
        end: date | str | None = None,
        auto_adjust: bool = False,
    ) -> dict:
        options = {"interval": interval, "auto_adjust": auto_adjust}
        if start is not None or end is not None:
            options["start"] = start
            options["end"] = end
        else:
            options["period"] = period

        history = yf.Ticker(ticker).history(**options)
        return map_price_history(ticker, history)
