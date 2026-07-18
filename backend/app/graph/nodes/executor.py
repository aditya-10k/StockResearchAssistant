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

def executor_node(state : GraphState):
    plan = state['execution_plan']
    required_services = set(plan.required_services)

    snapshots=[]
    news_results = {}
    financials_results = {}
    price_history_results = {}
    calendar_results = {}
    holders_results = {}
    recommendations_results = {}
    earnings_results = {}

    for company in plan.entities:
        ticker = company.ticker

        if ServiceType.MARKET in required_services:
            snapshots.append(market_service.get_company_snapshot(ticker))
        if ServiceType.NEWS in required_services:
            news_results[ticker] = news_service.get_company_news(ticker)
        if ServiceType.FINANCIALS in required_services:
            financials_results[ticker] = financials_service.get_financials(ticker)
        if ServiceType.PRICE_HISTORY in required_services:
            price_history_results[ticker] = price_history_service.get_price_history(ticker)
        if ServiceType.CALENDAR in required_services:
            calendar_results[ticker] = calendar_service.get_calendar(ticker)
        if ServiceType.HOLDERS in required_services:
            holders_results[ticker] = holders_service.get_holders(ticker)
        if ServiceType.RECOMMENDATIONS in required_services:
            recommendations_results[ticker] = recommendations_service.get_recommendations(ticker)
        if ServiceType.EARNINGS in required_services:
            earnings_results[ticker] = earnings_service.get_earnings(ticker)

    return{
    "market_data" : snapshots,
    "news_data" : news_results,
    "financials_data": financials_results,
    "price_history_data": price_history_results,
    "calendar_data": calendar_results,
    "holders_data": holders_results,
    "recommendations_data": recommendations_results,
    "earnings_data": earnings_results,
    }
