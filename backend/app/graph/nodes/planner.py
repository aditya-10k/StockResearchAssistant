from app.graph.state import GraphState
from app.ai.planner.planner_service import PlannerService

planner_service = PlannerService()

def planner(state : GraphState):
    
    execution_plan = planner_service.create_plan(
        state["query"]
    )

    return {
        "execution_plan" : execution_plan
    }