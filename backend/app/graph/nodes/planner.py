from app.graph.state import GraphState

def planner(state : GraphState):
    print("Planner Node executted")
    print(state)
    return {
        "query" : state["query"]
    }