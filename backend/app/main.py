from fastapi import FastAPI
from app.schemas.query import QueryReq
from app.api.router import main_router
from app.core.config import settings
from app.db.database import engine, Base
from sqlalchemy import text

# Create tables & seed RAG documents
try:
    if "postgresql" in engine.url.drivername:
        try:
            with engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                conn.commit()
        except Exception as ve:
            print(f"Notice: pgvector extension creation skipped: {ve}")
    Base.metadata.create_all(bind=engine)
    
    # Auto-seed reference research documents if empty
    from app.db.database import SessionLocal
    from app.ai.rag.service import RAGService
    with SessionLocal() as seed_db:
        RAGService(seed_db).seed_initial_documents()
except Exception as e:
    print(f"Warning: Database initialization skipped or failed: {e}")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title= settings.APP_NAME,
    version=settings.APP_VER
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

@app.get("/")
@app.head("/")
def root():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VER}

@app.get("/health")
@app.head("/health")
def health():
    return {"status": "ok", "service": "Stock Research Assistant API"}