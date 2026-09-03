from app.graph.state import GraphState
from app.ai.llm.service import LLMService
from app.ai.llm.models import LLMRequest

llm = LLMService()

def verification_node(state: GraphState):
    prompt = f"Verify the following analysis against the provided data.\n\nAnalysis: {state['analysis']}\n\nData: {state['market_data']}\n\nDoes the analysis accurately reflect the data? Provide a short verification summary."
    
    request = LLMRequest(
        system_prompt="You are a strict compliance and verification officer.",
        user_prompt=prompt
    )
    result = llm.generate(request)
    
    return {
        "verification_result": result
    }
