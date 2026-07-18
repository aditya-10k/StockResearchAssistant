import yfinance as yf

from app.services.financials.mapper import map_financials


class FinancialsService:
    def get_financials(self, ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        financials = {
            "annual_income_statement": stock.financials,
            "quarterly_income_statement": stock.quarterly_financials,
            "annual_balance_sheet": stock.balance_sheet,
            "quarterly_balance_sheet": stock.quarterly_balance_sheet,
            "annual_cash_flow": stock.cashflow,
            "quarterly_cash_flow": stock.quarterly_cashflow,
        }
        return map_financials(ticker, financials)
