import json
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ChatSession, ChatMessage

router = APIRouter(prefix="/chats", tags=["chats"])


class CreateSessionReq(BaseModel):
    title: Optional[str] = None
    is_public: bool = True


class AddMessageReq(BaseModel):
    role: str  # "user" or "assistant"
    content: Optional[str] = None
    structured_payload: Optional[dict] = None


@router.post("", status_code=status.HTTP_201_CREATED)
def create_session(req: CreateSessionReq = None, db: Session = Depends(get_db)):
    """Create a new chat research session."""
    session_id = uuid.uuid4().hex[:12]
    title = (req.title if req and req.title else "New Research").strip()
    is_public = req.is_public if req else True

    try:
        session = ChatSession(
            id=session_id,
            title=title,
            is_public=is_public,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return {
            "id": session.id,
            "title": session.title,
            "is_public": session.is_public,
            "created_at": session.created_at.isoformat() if session.created_at else None,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("")
def list_sessions(limit: int = 30, db: Session = Depends(get_db)):
    """List recent research sessions for the frontend sidebar."""
    try:
        sessions = (
            db.query(ChatSession)
            .order_by(ChatSession.updated_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": s.id,
                "title": s.title,
                "is_public": s.is_public,
                "message_count": len(s.messages) if s.messages else 0,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "updated_at": s.updated_at.isoformat() if s.updated_at else None,
            }
            for s in sessions
        ]
    except Exception as e:
        # Graceful return if DB is unavailable
        return []


@router.get("/{session_id}")
def get_session(session_id: str, db: Session = Depends(get_db)):
    """Retrieve full chat session including message history and structured research payloads."""
    try:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")

        messages_data = []
        for msg in session.messages:
            payload = None
            if msg.structured_payload:
                try:
                    payload = json.loads(msg.structured_payload)
                except Exception:
                    payload = None

            messages_data.append({
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "structured_payload": payload,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
            })

        return {
            "id": session.id,
            "title": session.title,
            "is_public": session.is_public,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "messages": messages_data,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/{session_id}/messages", status_code=status.HTTP_201_CREATED)
def add_message(session_id: str, req: AddMessageReq, db: Session = Depends(get_db)):
    """Add a user query or assistant structured response to a chat session."""
    try:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            # Auto-create session if it doesn't exist
            title = "New Research"
            if req.role == "user" and req.content:
                title = req.content[:35] + ("..." if len(req.content) > 35 else "")
            session = ChatSession(id=session_id, title=title, is_public=True)
            db.add(session)
            db.commit()
            db.refresh(session)
        elif req.role == "user" and session.title == "New Research" and req.content:
            # Auto-update session title from first user query
            session.title = req.content[:35] + ("..." if len(req.content) > 35 else "")

        payload_str = json.dumps(req.structured_payload) if req.structured_payload else None

        msg = ChatMessage(
            session_id=session_id,
            role=req.role,
            content=req.content,
            structured_payload=payload_str,
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)

        return {
            "id": msg.id,
            "session_id": msg.session_id,
            "role": msg.role,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/share/{session_id}")
def get_shared_session(session_id: str, db: Session = Depends(get_db)):
    """Public read-only endpoint for viewing and sharing a completed research report."""
    try:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Shared research report not found")
        if not session.is_public:
            raise HTTPException(status_code=403, detail="This research report is private")

        messages_data = []
        for msg in session.messages:
            payload = None
            if msg.structured_payload:
                try:
                    payload = json.loads(msg.structured_payload)
                except Exception:
                    payload = None

            messages_data.append({
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "structured_payload": payload,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
            })

        return {
            "id": session.id,
            "title": session.title,
            "is_public": session.is_public,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "messages": messages_data,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a research session."""
    try:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        db.delete(session)
        db.commit()
        return {"status": "deleted", "id": session_id}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
