from app.graph.state import GraphState
from app.services.market.service import MarketService
from app.services.news.service import NewsService
from app.services.financials.service import FinancialsService
from app.services.price_history.service import PriceHistoryService
from app.services.calendar.service import CalendarService
from app.services.holders.service import HoldersService
from app.services.recommendations.service import RecommendationsService
from app.services.earnings.service import EarningsService
from app.schemas.execution_plan import ServiceType

market_service = MarketService()
news_service = NewsService()
financials_service = FinancialsService()
price_history_service = PriceHistoryService()
calendar_service = CalendarService()
holders_service = HoldersService()
recommendations_service = RecommendationsService()
earnings_service = EarningsService()

def executor_node(state: GraphState):
    plan = state['execution_plan']
    required_services = set(plan.required_services)

    snapshots = []
    news_results = {}
    financials_results = {}
    price_history_results = {}
    calendar_results = {}
    holders_results = {}
    recommendations_results = {}
    earnings_results = {}

    for company in plan.entities:
        ticker = company.ticker

        # 1. Market Data (Always attempt snapshot)
        if ServiceType.MARKET in required_services:
            try:
                snapshots.append(market_service.get_company_snapshot(ticker))
            except Exception as e:
                print(f"[executor] Market snapshot error for {ticker}: {e}")

        # 2. News Data
        if ServiceType.NEWS in required_services:
            try:
                news_results[ticker] = news_service.get_company_news(ticker)
            except Exception as e:
                print(f"[executor] News error for {ticker}: {e}")
                news_results[ticker] = []

        # 3. Financials
        if ServiceType.FINANCIALS in required_services:
            try:
                financials_results[ticker] = financials_service.get_financials(ticker)
            except Exception as e:
                print(f"[executor] Financials error for {ticker}: {e}")

        # 4. Price History
        if ServiceType.PRICE_HISTORY in required_services:
            try:
                price_history_results[ticker] = price_history_service.get_price_history(ticker)
            except Exception as e:
                print(f"[executor] Price history error for {ticker}: {e}")

        # 5. Calendar
        if ServiceType.CALENDAR in required_services:
            try:
                calendar_results[ticker] = calendar_service.get_calendar(ticker)
            except Exception as e:
                print(f"[executor] Calendar error for {ticker}: {e}")

        # 6. Holders
        if ServiceType.HOLDERS in required_services:
            try:
                holders_results[ticker] = holders_service.get_holders(ticker)
            except Exception as e:
                print(f"[executor] Holders error for {ticker}: {e}")

        # 7. Recommendations
        if ServiceType.RECOMMENDATIONS in required_services:
            try:
                recommendations_results[ticker] = recommendations_service.get_recommendations(ticker)
            except Exception as e:
                print(f"[executor] Recommendations error for {ticker}: {e}")

        # 8. Earnings
        if ServiceType.EARNINGS in required_services:
            try:
                earnings_results[ticker] = earnings_service.get_earnings(ticker)
            except Exception as e:
                print(f"[executor] Earnings error for {ticker}: {e}")

    return {
        "market_data": snapshots,
        "news_data": news_results,
        "financials_data": financials_results,
        "price_history_data": price_history_results,
        "calendar_data": calendar_results,
        "holders_data": holders_results,
        "recommendations_data": recommendations_results,
        "earnings_data": earnings_results,
    }
