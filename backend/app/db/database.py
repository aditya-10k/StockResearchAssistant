from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Safe connection parameters for cloud & containerized PostgreSQL
db_url = settings.DATABASE_URL or "postgresql://postgres:postgres@127.0.0.1:5433/stock_db"
engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

