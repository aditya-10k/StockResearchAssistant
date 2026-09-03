from sqlalchemy.orm import Session
from app.db.models import ResearchDocument
from google import genai
from app.core.config import settings

class RAGService:
    def __init__(self, db: Session):
        self.db = db
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_embedding(self, text: str) -> list[float]:
        result = self.client.models.embed_content(
            model='text-embedding-004',
            contents=text,
        )
        return result.embeddings[0].values

    def add_document(self, title: str, content: str):
        embedding = self.get_embedding(content)
        doc = ResearchDocument(title=title, content=content, embedding=embedding)
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def search_documents(self, query: str, limit: int = 3) -> list[ResearchDocument]:
        query_embedding = self.get_embedding(query)
        # Using pgvector L2 distance operator (<->)
        results = self.db.query(ResearchDocument).order_by(
            ResearchDocument.embedding.l2_distance(query_embedding)
        ).limit(limit).all()
        return results
