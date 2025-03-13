from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import scraper, retrieval, chat, urls

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",  # Next.js development server
    "http://localhost:3000",  # Sometimes it's accessed via localhost
]

# Enable CORS so Next.js frontend can communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Update this to your frontend URL in production
    #allow_origins=[os.getenv("NEXT_PUBLIC_FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the scraper API
app.include_router(urls.router, prefix="/api")
app.include_router(scraper.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(retrieval.router, prefix="/api")   #Basically for testing storage & retrieval of embedded contents into the FAISS vector database

@app.get("/")
def home():
    return {"message": "RAG Conversational Bot API is running!"}
