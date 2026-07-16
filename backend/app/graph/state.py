from typing import TypedDict
from app.schemas.execution_plan import ExecutionPlan

class GraphState(TypedDict):
    query : str
    execution_plan : ExecutionPlan | None
