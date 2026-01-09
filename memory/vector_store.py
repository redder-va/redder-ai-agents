from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

# Lazy initialization to speed up imports
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return _embeddings

def get_vector_store():
    embeddings = get_embeddings()
    if os.path.exists("memory/faiss_index"):
        vector_store = FAISS.load_local("memory/faiss_index", embeddings, allow_dangerous_deserialization=True)
    else:
        # Create empty store
        vector_store = FAISS.from_texts(["initial"], embeddings)
    return vector_store

def save_vector_store(vector_store):
    vector_store.save_local("memory/faiss_index")