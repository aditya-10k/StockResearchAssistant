from langgraph.graph import START ,END , StateGraph
from app.graph.state import GraphState
from app.graph.nodes.planner import planner

builder = StateGraph(GraphState)

builder.add_node("planner" ,planner)
builder.add_edge(START , "planner")
builder.add_edge("planner" , END)

query_graph = builder.compile()