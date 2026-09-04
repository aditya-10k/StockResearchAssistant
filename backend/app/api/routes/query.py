import json

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse

from app.schemas.query import QueryReq
from app.graph.builder import query_graph


router = APIRouter()


import uuid

@router.post("/query/stream")
def query_stream(request: QueryReq):
    """Stream each completed LangGraph node update as a server-sent event, and persist to Postgres."""

    def event_generator():
        session_id = request.session_id or uuid.uuid4().hex[:12]
        yield f"event: session\ndata: {json.dumps({'session_id': session_id})}\n\n"

        inputs = {
            "query": request.query,
            "chat_history": request.chat_history,
            "execution_plan": None,
        }

        final_market_data = []
        final_news_data = {}
        final_analysis = None
        final_verification = None

        try:
            for update in query_graph.stream(inputs, stream_mode="updates"):
                node_name, node_data = next(iter(update.items()))
                
                # Capture final data for database persistence
                if isinstance(node_data, dict):
                    if "market_data" in node_data and node_data["market_data"]:
                        final_market_data = node_data["market_data"]
                    if "news_data" in node_data and node_data["news_data"]:
                        final_news_data = node_data["news_data"]
                    if "analysis" in node_data and node_data["analysis"]:
                        final_analysis = node_data["analysis"]
                    if "verification_result" in node_data:
                        final_verification = node_data["verification_result"]

                payload = json.dumps(jsonable_encoder(node_data))
                yield f"event: {node_name}\ndata: {payload}\n\n"

            yield f"event: done\ndata: {json.dumps({'session_id': session_id})}\n\n"

            # Persist chat history and index research verdict to PostgreSQL
            try:
                from app.db.database import SessionLocal
                from app.db.models import ChatSession, ChatMessage
                from app.ai.rag.service import RAGService

                with SessionLocal() as db:
                    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
                    title = request.query[:35] + ("..." if len(request.query) > 35 else "")
                    if not session:
                        session = ChatSession(id=session_id, title=title, is_public=True)
                        db.add(session)
                        db.commit()
                    elif session.title == "New Research":
                        session.title = title
                        db.commit()

                    # Save user query
                    user_msg = ChatMessage(session_id=session_id, role="user", content=request.query)
                    db.add(user_msg)

                    # Save assistant structured response
                    structured = {
                        "market_data": jsonable_encoder(final_market_data),
                        "news_data": jsonable_encoder(final_news_data),
                        "analysis": jsonable_encoder(final_analysis),
                        "verification_result": final_verification,
                    }
                    summary = final_analysis.get("summary", "") if isinstance(final_analysis, dict) else ""
                    asst_msg = ChatMessage(
                        session_id=session_id,
                        role="assistant",
                        content=str(summary),
                        structured_payload=json.dumps(structured),
                    )
                    db.add(asst_msg)
                    db.commit()

                    # Auto-index research verdict into RAG Knowledge Base
                    if isinstance(final_analysis, dict) and final_analysis.get("conclusion"):
                        rag = RAGService(db)
                        rag.add_document(
                            title=f"Verdict: {session.title}",
                            content=f"Query: {request.query}\nVerdict: {final_analysis.get('conclusion')}\nThesis: {final_analysis.get('investment_thesis', '')}",
                            doc_type="past_verdict",
                        )
            except Exception as db_err:
                print(f"[query_stream] Chat DB save skipped: {db_err}")

        except Exception as error:
            import traceback
            traceback.print_exc()
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
