import yfinance as yf
import requests
from app.services.recommendations.mapper import map_recommendations

_session = requests.Session()
_session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
})


class RecommendationsService:
    def get_recommendations(self, ticker: str) -> dict:
        try:
            stock = yf.Ticker(ticker, session=_session)
        except Exception:
            stock = yf.Ticker(ticker)

        recommendations = {}
        try:
            recommendations["recommendations"] = stock.recommendations
        except Exception:
            recommendations["recommendations"] = None

        try:
            recommendations["recommendations_summary"] = stock.recommendations_summary
        except Exception:
            recommendations["recommendations_summary"] = None

        try:
            recommendations["upgrades_downgrades"] = stock.upgrades_downgrades
        except Exception:
            recommendations["upgrades_downgrades"] = None

        try:
            return map_recommendations(ticker, recommendations)
        except Exception:
            return {}
