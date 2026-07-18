import yfinance as yf

from app.services.holders.mapper import map_holders


class HoldersService:
    def get_holders(self, ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        holders = {
            "major_holders": stock.major_holders,
            "institutional_holders": stock.institutional_holders,
            "mutualfund_holders": stock.mutualfund_holders,
            "insider_transactions": stock.insider_transactions,
            "insider_purchases": stock.insider_purchases,
            "insider_roster_holders": stock.insider_roster_holders,
        }
        return map_holders(ticker, holders)
