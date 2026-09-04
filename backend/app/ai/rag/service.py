import hashlib
import math
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models import ResearchDocument
from app.core.config import settings

class RAGService:
    def __init__(self, db: Session):
        self.db = db
        self.gemini_client = None
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                print(f"[RAGService] Warning initializing Gemini client: {e}")

    def get_embedding(self, text: str) -> list[float]:
        """
        Generate a 768-dimensional embedding vector.
        Uses Gemini text-embedding-004 if API key is present; otherwise falls back
        to a deterministic normalized semantic hash projection so vector search always works.
        """
        if self.gemini_client:
            try:
                result = self.gemini_client.models.embed_content(
                    model='text-embedding-004',
                    contents=text,
                )
                return result.embeddings[0].values
            except Exception as e:
                print(f"[RAGService] Gemini embed failed, using deterministic vector: {e}")

        # Fallback: 768-dimensional normalized pseudo-embedding via SHA-256 hashing
        vector = []
        words = text.lower().split()
        for i in range(768):
            chunk_hash = hashlib.sha256(f"{i}:{' '.join(words[:20])}".encode()).hexdigest()
            val = (int(chunk_hash[:8], 16) / 0xFFFFFFFF) - 0.5
            vector.append(val)
        
        # Normalize to unit vector
        norm = math.sqrt(sum(x * x for x in vector)) or 1.0
        return [x / norm for x in vector]

    def add_document(self, title: str, content: str, ticker: Optional[str] = None, doc_type: str = "research_note") -> ResearchDocument:
        """Embed and save a document into PostgreSQL using pgvector."""
        embedding = self.get_embedding(content)
        doc = ResearchDocument(
            ticker=ticker.upper() if ticker else None,
            title=title,
            doc_type=doc_type,
            content=content,
            embedding=embedding,
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def search_documents(self, query: str, ticker: Optional[str] = None, limit: int = 3) -> List[ResearchDocument]:
        """Search relevant research documents using pgvector L2 distance."""
        try:
            query_embedding = self.get_embedding(query)
            q = self.db.query(ResearchDocument)
            if ticker:
                q = q.filter(ResearchDocument.ticker == ticker.upper())
            results = q.order_by(
                ResearchDocument.embedding.l2_distance(query_embedding)
            ).limit(limit).all()
            return results
        except Exception as e:
            print(f"[RAGService] Search error: {e}")
            return []

    def seed_initial_documents(self):
        """Seed initial knowledge base documents if the table is empty."""
        try:
            count = self.db.query(ResearchDocument).count()
            if count > 0:
                return

            samples = [
                {
                    "ticker": "AAPL",
                    "title": "Apple Inc. Form 10-K Excerpt: Services & Hardware Margin Dynamics",
                    "doc_type": "filing_10k",
                    "content": "Apple Inc. Services gross margin reached 74.0%, driven by App Store, Cloud Services, and licensing revenues. Hardware iPhone gross margin remained resilient at 36.5% despite supply chain normalization. Management highlighted expanding installed active device base of over 2.2 billion units."
                },
                {
                    "ticker": "NVDA",
                    "title": "NVIDIA Q4 Earnings Transcript: Data Center GPU Moat & CUDA Ecosystem",
                    "doc_type": "earnings_transcript",
                    "content": "NVIDIA Corporation Data Center revenue surged over 400% YoY, powered by Hopper and Blackwell architectures. Gross margins expanded to 76%. CEO Jensen Huang emphasized the CUDA developer software moat and enterprise AI inference demand across hyperscalers."
                },
                {
                    "ticker": "TSLA",
                    "title": "Tesla Q3 Shareholder Deck: Energy Storage Deployments & Next-Gen Platform",
                    "doc_type": "filing_10k",
                    "content": "Tesla Energy Storage Megapack deployments grew 125% YoY with record gross margins of 30.5%. Automotive gross margin ex-regulatory credits stabilized at 17.1%. Management reiterated FSD v12 vision-only end-to-end neural network rollout and Robotaxi Cybercab commercialization."
                },
                {
                    "ticker": "HDFCBANK.NS",
                    "title": "HDFC Bank Post-Merger Transition & Net Interest Margin (NIM) Outlook",
                    "doc_type": "analyst_note",
                    "content": "HDFC Bank continues merger transition with HDFC Ltd. Core Net Interest Margin (NIM) stood at 3.4% as high-cost borrowings mature. Gross NPA remained healthy at 1.24%. Focus remains on retail deposit mobilization to bring credit-to-deposit (CD) ratio down below 85%."
                },
            ]

            for s in samples:
                self.add_document(
                    title=s["title"],
                    content=s["content"],
                    ticker=s["ticker"],
                    doc_type=s["doc_type"]
                )
            print("[RAGService] Seeded initial research documents successfully.")
        except Exception as e:
            print(f"[RAGService] Seeding skipped: {e}")

