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
4. Grading relevance and correcting weak retrievals (Corrective RAG).
5. Creating embeddings.
6. Saving papers into ChromaDB.
"""

from backend.api.arxiv_api import search_arxiv
from backend.api.semantic_api import search_semantic_scholar
from backend.llm.embeddings import generate_embedding
from backend.database.chroma_db import add_paper
from backend.agents.corrective_rag_agent import grade_and_correct


def _raw_search(query: str):
    """
    Fetch papers from all sources without grading or storing.
    Used both for the initial search and for corrective re-search.
    """

    arxiv_results = search_arxiv(query)
    semantic_results = search_semantic_scholar(query)

    return arxiv_results + semantic_results


def search_papers(query: str):
    """
    Search research papers, apply Corrective RAG relevance
    grading, and save the surviving papers in ChromaDB.
    """

    print("=" * 50)
    print("Search Agent Started")
    print("=" * 50)

    all_papers = _raw_search(query)
    print(f"Retrieved {len(all_papers)} raw papers.")

    # ---------------------------------------------
    # Corrective RAG: grade relevance, correct if needed.
    # ---------------------------------------------
    all_papers = grade_and_correct(
        topic=query,
        papers=all_papers,
        research_fn=_raw_search
    )

    # ---------------------------------------------
    # Loop through every surviving paper.
    # ---------------------------------------------
    for index, paper in enumerate(all_papers):

        title = paper.get("title", "No Title")
        text = paper.get("summary") or paper.get("abstract") or ""
        embedding = generate_embedding(text)

        add_paper(
            # Title + index avoids ID collisions across separate runs,
            # unlike the previous plain str(index).
            paper_id=f"{title[:40]}-{index}",
            title=title,
            summary=text,
            embedding=embedding
        )

    print(f"{len(all_papers)} papers stored successfully.")

    return all_papers