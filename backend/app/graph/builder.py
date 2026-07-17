from langgraph.graph import START ,END , StateGraph
from app.graph.state import GraphState
from app.graph.nodes.planner import planner
from app.graph.nodes.executor import executor_node
from app.graph.nodes.analysis import analysis_node
from app.graph.nodes.guardrail import guardrail_node
from app.graph.nodes.blocked import blocked_node
from app.graph.routers import guardrail_router

builder = StateGraph(GraphState)

builder.add_node("guardrail", guardrail_node)
builder.add_node("planner" ,planner)
builder.add_node("executor" ,executor_node)
builder.add_node("analysis", analysis_node)
builder.add_node("blocked", blocked_node)

builder.add_edge(START , "guardrail")
builder.add_conditional_edges("guardrail",
                            guardrail_router,
                            {
                                "planner" :"planner",
                                "blocked": "blocked",
                              })
builder.add_edge("planner" , "executor")
builder.add_edge("executor" ,"analysis")
builder.add_edge("analysis"  ,END)
builder.add_edge("blocked" , END)

query_graph = builder.compile()