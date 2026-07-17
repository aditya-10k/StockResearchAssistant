from app.graph.state import GraphState

def blocked_node(state : GraphState) :

    return{
        'analysis' : {
            "summary" : state["guardrail"].response,
            "investment_thesis": "",
            "strengths": [],
            "risks": [],
            "valuation": "",
            "conclusion": ""
        }
    }