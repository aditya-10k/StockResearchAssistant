from fastapi import FastAPI
from app.schemas.query import QueryReq

app = FastAPI()

@app.get("/hi")
def working() :
    return "working"

@app.post("/stock")
def stock(request : QueryReq):
    return{
        "ans" : request.query 
    }