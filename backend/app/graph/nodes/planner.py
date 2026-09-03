from app.graph.state import GraphState
from app.ai.planner.planner_service import PlannerService

planner_service = PlannerService()

def planner(state : GraphState):
    query = state["query"]
    if state.get('chat_history'):
        history_str = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in state['chat_history']])
        query = f"Previous Conversation Context:\n{history_str}\n\nCurrent Query:\n{query}"

    execution_plan = planner_service.create_plan(query)

    return {
        "execution_plan" : execution_plan
    }