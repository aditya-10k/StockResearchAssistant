from pydantic import BaseModel

class QueryReq(BaseModel) :
    query : str