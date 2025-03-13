from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from app.models.chat_model import ChatRequest
from app.db.vector_store import search_faiss
# from app.db.vector_store import search_chroma
# from app.db.vector_store import search_pinecone
# from app.db.vector_store import search_mongo
from app.services.llm_service import generate_response

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
   
    # Generate AI response based on retrieved documents
    response = generate_response(request.query)

    return JSONResponse(content={ "ai_response": response })



#GET http://127.0.0.1:8000/api/chat?query=latest AI updates&db=faiss&llm=groq

@router.get("/chat")
def chat(query: str = Query(...), db: str = "faiss", top_k: int = 3, llm: str ="groq"):
    """
    Retrieve relevant documents from the vector database and generate an AI response.
    
    Args:
        query (str): The user's question.
        db (str): The vector database to use (faiss, chroma, pinecone, mongo).
        top_k (int): Number of top documents to retrieve.
    
    Returns:
        dict: Query, retrieved documents, and AI-generated response.
    """
    # Retrieve relevant documents
    if db == "faiss":
        retrieved_docs = search_faiss(query, top_k)
    # elif db == "chroma":
    #     retrieved_docs = search_chroma(query, top_k)
    # elif db == "pinecone":
    #     retrieved_docs = search_pinecone(query, top_k)
    # elif db == "mongo":
    #     retrieved_docs = search_mongo(query, top_k)
    else:
        return {"error": "Invalid database option"}

    # Generate AI response based on retrieved documents
    response = generate_response(query, retrieved_docs,llm)


    return {
        "ai_response": response
    }



