import yfinance as yf

from app.services.recommendations.mapper import map_recommendations


class RecommendationsService:
    def get_recommendations(self, ticker: str) -> dict:
        stock = yf.Ticker(ticker)
        recommendations = {
            "recommendations": stock.recommendations,
            "recommendations_summary": stock.recommendations_summary,
            "upgrades_downgrades": stock.upgrades_downgrades,
        }
        return map_recommendations(ticker, recommendations)
