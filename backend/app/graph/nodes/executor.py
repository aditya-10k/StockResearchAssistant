from app.graph.state import GraphState
from app.services.market.service import MarketService
from app.services.news.service import NewsService

market_service = MarketService()
news_service = NewsService()

def executor_node(state : GraphState):
    plan = state['execution_plan']

    snapshots=[]

    for company in plan.entities:
        snapshot = market_service.get_company_snapshot(
            company.ticker
        )
        snapshots.append(snapshot)
    
    news_results = {}
    
    for company in plan.entities :
        news_results[company.ticker] = news_service.get_company_news(company.ticker)

    return{
    "market_data" : snapshots,
    "news_data" : news_results
    }