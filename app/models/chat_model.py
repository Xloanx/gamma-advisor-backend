from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    db: str = "faiss"
    top_k: int = 3
    llm: str = "groq"