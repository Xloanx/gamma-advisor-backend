from fastapi import APIRouter, Query
from app.db.vector_store import store_data_faiss, search_faiss
# from app.db.vector_store import store_data_pinecone, search_pinecone, store_data_chroma, search_chroma
# from app.db.vector_store import store_data_mongo, search_mongo

router = APIRouter()


#POST http://127.0.0.1:8000/api/process-data/

@router.post("/process-data/")
def process_data():
    """Embed scraped data and store in vector database."""
    store_data_faiss()
    # store_data_chroma()
    # store_data_pinecone()
    # store_data_mongo()
    return {"message": "Scraped data processed and stored in vector databases!"}


#GET http://127.0.0.1:8000/api/search/?query=latest news&db=faiss
@router.get("/search/")
def search_documents(query: str = Query(...), top_k: int = 3, db: str = "faiss"):
    """Search for documents in the vector database."""
    if db == "faiss":
        results = search_faiss(query, top_k)
    else:
        return {"error": "Invalid database option"}

    return {"query": query, "results": results}
