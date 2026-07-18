import json

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse

from app.schemas.query import QueryReq
from app.graph.builder import query_graph


router = APIRouter()


@router.post("/query/stream")
def query_stream(request: QueryReq):
    """Stream each completed LangGraph node update as a server-sent event."""

    def event_generator():
        inputs = {
            "query": request.query,
            "execution_plan": None,
        }

        try:
            for update in query_graph.stream(inputs, stream_mode="updates"):
                node_name, node_data = next(iter(update.items()))
                payload = json.dumps(jsonable_encoder(node_data))

                yield f"event: {node_name}\ndata: {payload}\n\n"

            yield "event: done\ndata: {}\n\n"
        except Exception as error:
            payload = json.dumps({"message": str(error)})
            yield f"event: error\ndata: {payload}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/query")
def query(request : QueryReq):
    result = query_graph.invoke({
        "query" : request.query,
        "execution_plan": None
    })

    return jsonable_encoder({
        "query": result.get("query"),
        "guardrail": result.get("guardrail"),
        "execution_plan": result.get("execution_plan"),
        "services": {
            "market": result.get("market_data"),
            "news": result.get("news_data"),
            "financials": result.get("financials_data"),
            "price_history": result.get("price_history_data"),
            "calendar": result.get("calendar_data"),
            "holders": result.get("holders_data"),
            "recommendations": result.get("recommendations_data"),
            "earnings": result.get("earnings_data"),
        },
        "analysis": result.get("analysis"),
    })
