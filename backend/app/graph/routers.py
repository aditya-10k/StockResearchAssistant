from app.graph.state import GraphState
from app.ai.guardrails.models import GuardrailDecision

def guardrail_router(state :GraphState) :
    decision = state['guardrail'].decision

    if decision == GuardrailDecision.ALLOW:
        return "planner"
    return "blocked"