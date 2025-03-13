from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-west1-gcp")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-index")
##########Uncomment the following if your vector database is mongodb##################################
# MONGO_URI=os.getenv("MONGODB_URI")
# MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "rag_db")
# MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "documents")

# Connect to MongoDB
# client = MongoClient(MONGO_URI)
# db = client[MONGODB_DBNAME]
# collection = db[MONGODB_COLLECTION]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")