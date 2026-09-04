import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

def init_engine():
    # 1. Try PostgreSQL if DATABASE_URL is configured
    pg_url = settings.DATABASE_URL or os.environ.get("DATABASE_URL")
    if pg_url and not pg_url.startswith("sqlite"):
        if pg_url.startswith("postgres://"):
            pg_url = pg_url.replace("postgres://", "postgresql://", 1)
        try:
            pg_engine = create_engine(
                pg_url,
                pool_pre_ping=True,
                pool_recycle=300,
                connect_args={"connect_timeout": 4}
            )
            with pg_engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
            logger.info("Connected to configured PostgreSQL database successfully.")
            return pg_engine
        except Exception as e:
            logger.warning(f"Failed to connect to configured DATABASE_URL ({e}). Falling back.")

    # 2. Try local containerized PostgreSQL on 5433 or 5432 if in local dev
    for local_port in [5433, 5432]:
        try:
            local_url = f"postgresql://postgres:postgres@127.0.0.1:{local_port}/stock_db"
            test_engine = create_engine(local_url, connect_args={"connect_timeout": 2})
            with test_engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
            logger.info(f"Connected to local PostgreSQL on port {local_port}.")
            return test_engine
        except Exception:
            pass

    # 3. Bulletproof SQLite fallback (works on Render, Docker, or any container without external DB)
    sqlite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "stock_research.db"))
    sqlite_url = f"sqlite:///{sqlite_path}"
    logger.info(f"Using SQLite database fallback at {sqlite_url}")
    return create_engine(sqlite_url, connect_args={"check_same_thread": False})

engine = init_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


