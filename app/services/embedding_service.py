from sentence_transformers import SentenceTransformer

# Load a pre-trained model for text embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """Generate an embedding vector from text."""
    return embedding_model.encode(text).tolist()
