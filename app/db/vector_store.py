############This file implements FAISS, Chromadb, Pinecone and MongoDB (Pick any of choice)
#Vector Database dependencies
import faiss
import chromadb
from pinecone import Pinecone, ServerlessSpec
# import pinecone
#from pymongo import MongoClient  (moved to config.py)

import numpy as np
import json
import os

from app.services.embedding_service import get_embedding
from app.config import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX_NAME
# from app.config import client, db, collection

import logging
from app.db.database import get_all_scraped_data  # Fetch scraped data
#########################################FAISS IMPLEMENTATION######################


# Configuration
VECTOR_SIZE = 384
FAISS_INDEX_FILE = "data/faiss_index.bin"

logging.basicConfig(level=logging.INFO)

# Initialize FAISS index
index = faiss.IndexFlatL2(VECTOR_SIZE)

# Load FAISS index from disk if available
def load_faiss_index():
    """Loads FAISS index from disk if available."""
    global index
    if os.path.exists(FAISS_INDEX_FILE):
        try:
            logging.info("Loading FAISS index from disk...")
            index = faiss.read_index(FAISS_INDEX_FILE)
        except Exception as e:
            logging.error(f"Error loading FAISS index: {e}")

# Store scraped documents in memory
documents = []

def store_data_faiss():
    """Loads scraped data, generates embeddings, and stores them in FAISS."""
    global documents

    new_data = get_all_scraped_data()  # Fetch fresh scraped data
    if not new_data:
        logging.warning("No new data to store in FAISS.")
        return

    for item in new_data:
        if item not in documents:  # Avoid duplicates
            embedding = get_embedding(item["content"])
            index.add(np.array([embedding], dtype=np.float32))
            documents.append(item)

    # Save FAISS index to disk
    faiss.write_index(index, FAISS_INDEX_FILE)
    logging.info(f"Stored {len(new_data)} new documents in FAISS.")

def search_faiss(query: str, top_k: int = 3):
    """Search for the most relevant documents in FAISS."""
    if len(documents) == 0:
        logging.warning("No documents in FAISS to search.")
        return []

    query_embedding = np.array([get_embedding(query)], dtype=np.float32)
    distances, indices = index.search(query_embedding, top_k)

    results = [documents[i] for i in indices[0] if i < len(documents)]
    return results

# Load FAISS index at startup
load_faiss_index()

##########################################CHROMADB IMPLEMENTATION################



# Initialize ChromaDB Client
# client = chromadb.PersistentClient(path="../data/chroma_db")

# # Create or load a collection
# collection = client.get_or_create_collection(name="documents")

# def store_data_chroma():
#     """Load scraped data, generate embeddings, and store them in ChromaDB."""
#     with open("data/scraped_data.json", "r") as file:
#         data = json.load(file)

#     for idx, item in enumerate(data):
#         embedding = get_embedding(item["content"])
#         collection.add(
#             ids=[str(idx)], documents=[item["content"]], embeddings=[embedding]
#         )

# def search_chroma(query: str, top_k: int = 3):
#     """Search for the most relevant documents in ChromaDB."""
#     query_embedding = get_embedding(query)
#     results = collection.query(query_embedding, n_results=top_k)

#     return [{"content": doc} for doc in results["documents"]]


######################################################PINECONE IMPLEMENTATION############################################

# Initialize Pinecone

# pc = Pinecone(
#     api_key=os.getenv("PINECONE_API_KEY")
# )

# # Create or connect to an index
# if 'my_index' not in pc.list_indexes().names():
#         pc.create_index(
#             name='my_index', 
#             dimension=1536, 
#             metric='euclidean',
#             spec=ServerlessSpec(
#                 cloud='aws',
#                 region='us-west-2'
#             )
#         )

# index = pc.Index(PINECONE_INDEX_NAME)

# def store_data_pinecone():
#     """Load scraped data, generate embeddings, and store in Pinecone."""
#     with open("data/scraped_data.json", "r") as file:
#         data = json.load(file)

#     vectors = []
#     for idx, item in enumerate(data):
#         embedding = get_embedding(item["content"])
#         vectors.append((str(idx), embedding, {"content": item["content"]}))

#     index.upsert(vectors)

# def search_pinecone(query: str, top_k: int = 3):
#     """Search for the most relevant documents in Pinecone."""
#     query_embedding = get_embedding(query)
#     results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

#     return [{"content": match["metadata"]["content"]} for match in results["matches"]]


###################################################MONGODB IMPLEMENTATION##########################################################

# def store_data_mongo():
#     """Load scraped data, generate embeddings, and store in MongoDB."""
#     with open("data/scraped_data.json", "r") as file:
#         data = json.load(file)

#     documents = []
#     for item in data:
#         embedding = get_embedding(item["content"])
#         documents.append({"content": item["content"], "embedding": embedding})

#     collection.insert_many(documents)

# def search_mongo(query: str, top_k: int = 3):
#     """Search for relevant documents using MongoDB Vector Search."""
#     query_embedding = get_embedding(query)

#     pipeline = [
#         {
#             "$vectorSearch": {
#                 "queryVector": query_embedding,
#                 "path": "embedding",
#                 "numCandidates": top_k,
#                 "limit": top_k
#             }
#         }
#     ]

#     results = collection.aggregate(pipeline)
#     return [{"content": doc["content"]} for doc in results]

