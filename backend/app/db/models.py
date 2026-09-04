from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import func
from app.db.database import Base

class ResearchDocument(Base):
    __tablename__ = "research_documents"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True, nullable=True)
    title = Column(String, index=True)
    doc_type = Column(String, default="research_note")  # filing, transcript, analyst_note, verdict
    content = Column(Text)
    embedding = Column(Vector(768))  # 768 dimensions for Gemini / high-res embeddings
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False, default="New Research")
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("chat_sessions.id", ondelete="CASCADE"), index=True)
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=True)
    structured_payload = Column(Text, nullable=True)  # JSON-encoded market_data, news_data, analysis, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ChatSession", back_populates="messages")

# Backwards compatibility alias
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

