from app.graph.state import GraphState
from app.analysis.service import AnalysisService

analysis_service = AnalysisService()

def analysis_node (state: GraphState) :

    analysis = analysis_service.analyze(
        query= state['query'],
        execution_plan= state["execution_plan"],

        market_data= state['market_data'],

        news_data= state["news_data"],
    )

    return{
        "analysis" : analysis
    }