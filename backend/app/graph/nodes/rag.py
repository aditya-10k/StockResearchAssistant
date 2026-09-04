from app.graph.state import GraphState
from app.db.database import SessionLocal
from app.ai.rag.service import RAGService

def rag_node(state: GraphState):
    """
    RAG node: searches PostgreSQL vector store for historical research notes,
    filings, and past verdicts for the companies being researched.
    """
    query = state.get("query", "")
    plan = state.get("execution_plan")
    entities = plan.entities if plan and plan.entities else []

    rag_docs = []

    db = None
    try:
        db = SessionLocal()
        rag_service = RAGService(db)

        # 1. Search for each entity's specific ticker context
        seen_ids = set()
        for ent in entities:
            ticker = ent.ticker
            results = rag_service.search_documents(query, ticker=ticker, limit=2)
            for r in results:
                if r.id not in seen_ids:
                    seen_ids.add(r.id)
                    rag_docs.append({
                        "id": r.id,
                        "title": r.title,
                        "ticker": r.ticker,
                        "doc_type": r.doc_type,
                        "content": r.content,
                    })

        # 2. General query semantic search if fewer than 3 docs found
        if len(rag_docs) < 3:
            general_results = rag_service.search_documents(query, limit=3 - len(rag_docs))
            for r in general_results:
                if r.id not in seen_ids:
                    seen_ids.add(r.id)
                    rag_docs.append({
                        "id": r.id,
                        "title": r.title,
                        "ticker": r.ticker,
                        "doc_type": r.doc_type,
                        "content": r.content,
                    })
    except Exception as e:
        print(f"[rag_node] Note: RAG search skipped (database may not be mounted): {e}")
    finally:
        if db:
            db.close()

    return {
        "rag_documents": rag_docs
    }
