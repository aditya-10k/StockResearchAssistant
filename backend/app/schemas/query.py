from pydantic import BaseModel

class QueryReq(BaseModel):
    query: str
    chat_history: list[dict] | None = None