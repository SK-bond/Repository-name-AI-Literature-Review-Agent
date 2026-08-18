"""
=========================================================
Search Agent
=========================================================

Purpose
-------
This agent is responsible for:

1. Searching papers from arXiv.
2. Searching papers from Semantic Scholar.
3. Combining all papers.
4. Creating embeddings.
5. Saving papers into ChromaDB.
"""

# -------------------------------------------------------
# Import arXiv search function.
# -------------------------------------------------------
from backend.api.arxiv_api import search_arxiv

# -------------------------------------------------------
# Import Semantic Scholar search function.
# -------------------------------------------------------
from backend.api.semantic_api import search_semantic_scholar

# -------------------------------------------------------
# Import embedding generator.
# -------------------------------------------------------
from backend.llm.embeddings import generate_embedding

# -------------------------------------------------------
# Import ChromaDB storage function.
# -------------------------------------------------------
from backend.database.chroma_db import add_paper


# -------------------------------------------------------
# Search Agent Function
# -------------------------------------------------------
def search_papers(query: str):
    """
    Search research papers and save them in ChromaDB.
    """

    print("=" * 50)
    print("Search Agent Started")
    print("=" * 50)

    # ---------------------------------------------
    # Search papers from arXiv.
    # ---------------------------------------------
    arxiv_results = search_arxiv(query)

    # ---------------------------------------------
    # Search papers from Semantic Scholar.
    # ---------------------------------------------
    semantic_results = search_semantic_scholar(query)

    # ---------------------------------------------
    # Combine both lists.
    # ---------------------------------------------
    all_papers = arxiv_results + semantic_results

    # ---------------------------------------------
    # Loop through every paper.
    # ---------------------------------------------
    for index, paper in enumerate(all_papers):

        # -----------------------------------------
        # Paper title.
        # -----------------------------------------
        title = paper.get("title", "No Title")

        # -----------------------------------------
        # Paper text.
        # -----------------------------------------
        text = paper.get("summary") or paper.get("abstract") or ""

        # -----------------------------------------
        # Generate embedding.
        # -----------------------------------------
        embedding = generate_embedding(text)

        # -----------------------------------------
        # Save into ChromaDB.
        # -----------------------------------------
        add_paper(
            paper_id=str(index),
            title=title,
            summary=text,
            embedding=embedding
        )

    print(f"{len(all_papers)} papers stored successfully.")

    # ---------------------------------------------
    # Return all papers.
    # ---------------------------------------------
    return all_papers