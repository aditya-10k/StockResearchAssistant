import yfinance as yf

from app.services.earnings.mapper import map_earnings


class EarningsService:
    def get_earnings(self, ticker: str, limit: int = 12) -> dict:
        stock = yf.Ticker(ticker)
        earnings = {
            "earnings_dates": stock.get_earnings_dates(limit=limit),
            "annual_earnings": stock.earnings,
            "quarterly_earnings": stock.quarterly_earnings,
        }
        return map_earnings(ticker, earnings)
