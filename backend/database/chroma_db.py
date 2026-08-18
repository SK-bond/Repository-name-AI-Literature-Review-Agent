"""
=========================================================
ChromaDB Module
=========================================================

Purpose:
--------
This file creates and manages the ChromaDB vector database.

Responsibilities:
1. Create a collection.
2. Store research papers.
3. Store embeddings.
4. Search similar papers.
"""

# -------------------------------------------------------
# Import ChromaDB.
# This library provides the vector database.
# -------------------------------------------------------
import chromadb

# -------------------------------------------------------
# Import configuration values.
# -------------------------------------------------------
from backend.config import CHROMA_COLLECTION

# -------------------------------------------------------
# Create a ChromaDB client.
# This manages the local database.
# -------------------------------------------------------
client = chromadb.Client()

# -------------------------------------------------------
# Create (or load) a collection.
# If the collection already exists, ChromaDB loads it.
# Otherwise, it creates a new one.
# -------------------------------------------------------
collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION
)

# -------------------------------------------------------
# Function: add_paper
# Adds a research paper and its embedding to ChromaDB.
# -------------------------------------------------------
def add_paper(paper_id: str, title: str, summary: str, embedding: list):
    """
    Store one research paper in ChromaDB.
    """

    collection.add(

        # Unique ID for each paper.
        ids=[paper_id],

        # Text document stored in the database.
        documents=[summary],

        # Numerical embedding vector.
        embeddings=[embedding],

        # Extra information (metadata).
        metadatas=[
            {
                "title": title
            }
        ]
    )

# -------------------------------------------------------
# Function: search_similar
# Finds papers similar to a query embedding.
# -------------------------------------------------------
def search_similar(query_embedding: list, top_k: int = 5):
    """
    Search for similar research papers.
    """

    results = collection.query(

        # Query embedding.
        query_embeddings=[query_embedding],

        # Number of results to return.
        n_results=top_k
    )

    return results