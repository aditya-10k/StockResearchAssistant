from fastapi import APIRouter
from app.schemas.query import QueryReq
from app.graph.builder import query_graph
from app.ai.llm.service import LLMService
from app.ai.llm.models import LLMRequest


llm = LLMService()


router = APIRouter()


# @router.post("/query")
# def query(request : QueryReq):
#     result = query_graph.invoke({
#         "query" : request.query
#     })
#     return result

@router.post("/query")
def query(request : QueryReq):
    response = llm.generate(
        LLMRequest(
            system_prompt="You are a finance assistant",
            user_prompt= request.query
        )
)
    return {
        "response" : response
    }