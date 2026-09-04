from fastapi import FastAPI
from app.schemas.query import QueryReq
from app.api.router import main_router
from app.core.config import settings
from app.db.database import engine, Base
from sqlalchemy import text

# Create tables (graceful for cloud deployment without local Postgres)
try:
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Database connection skipped or failed: {e}")

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