import yfinance as yf

from app.services.calendar.mapper import map_calendar


class CalendarService:
    def get_calendar(self, ticker: str):
        stock = yf.Ticker(ticker)
        return map_calendar(ticker, stock.calendar)
