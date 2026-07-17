from fastapi import APIRouter
from app.schemas.query import QueryReq
from app.graph.builder import query_graph
from app.ai.llm.service import LLMService
from app.ai.llm.models import LLMRequest
from app.ai.guardrails.models import GuardrailDecision


llm = LLMService()


router = APIRouter()


@router.post("/query")
def query(request : QueryReq):
    result = query_graph.invoke({
        "query" : request.query,
        "execution_plan": None
    })
    if result["guardrail"].decision != GuardrailDecision.ALLOW:
        return {
            "message": result["guardrail"].response
        }

    return result["analysis"]

# @router.post("/query")
# def query(request : QueryReq):
#     response = llm.generate(
#         LLMRequest(
#             system_prompt="You are a finance assistant",
#             user_prompt= request.query
#         )
# )
#     return {
#         "response" : response
#     }