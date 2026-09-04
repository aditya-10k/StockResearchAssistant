from app.graph.state import GraphState
from app.analysis.service import AnalysisService

analysis_service = AnalysisService()

def analysis_node (state: GraphState) :
    query = state['query']

    # Inject RAG reference documents if retrieved
    rag_docs = state.get('rag_documents') or []
    if rag_docs:
        rag_str = "\n\n".join([f"[{d.get('title', 'Reference Document')}]: {d.get('content', '')}" for d in rag_docs])
        query = f"Reference Grounding Documents:\n{rag_str}\n\n{query}"

    if state.get('chat_history'):
        history_str = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in state['chat_history']])
        query = f"Previous Conversation Context:\n{history_str}\n\n{query}"

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
