import yfinance as yf
from app.services.market.mapper import map_company_snapshot

class MarketService:

    def get_company_snapshot(self , ticker : str):

        stock = yf.Ticker(ticker)
        info = stock.info

        return map_company_snapshot(
            ticker , info
        )