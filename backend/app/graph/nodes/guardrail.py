from app.graph.state import GraphState
from app.ai.guardrails.service import GuardrailService

guardrail_service = GuardrailService()

def guardrail_node(state : GraphState) :

    result = guardrail_service.validate(
        state['query']
    )
    print(result)


    return{
        "guardrail" : result
    }