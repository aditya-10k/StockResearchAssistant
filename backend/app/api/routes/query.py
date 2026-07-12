from fastapi import APIRouter
from app.schemas.query import QueryReq

router = APIRouter()

@router.post("/query")
def query(request : QueryReq):
    return{
        "stock" : request.query
    }