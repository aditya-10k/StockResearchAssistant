from app.graph.state import GraphState
from app.analysis.service import AnalysisService

analysis_service = AnalysisService()

def analysis_node (state: GraphState) :
    query = state['query']
    if state.get('chat_history'):
        history_str = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in state['chat_history']])
        query = f"Previous Conversation Context:\n{history_str}\n\nCurrent Query:\n{query}"

    analysis = analysis_service.analyze(
        query= query,
        execution_plan= state["execution_plan"],

        market_data= state['market_data'],
        news_data= state["news_data"],
        financials_data=state["financials_data"],
        price_history_data=state["price_history_data"],
        calendar_data=state["calendar_data"],
        holders_data=state["holders_data"],
        recommendations_data=state["recommendations_data"],
        earnings_data=state["earnings_data"],
    )

    return{
        "analysis" : analysis
    }
