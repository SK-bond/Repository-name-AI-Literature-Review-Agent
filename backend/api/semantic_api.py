"""
====================================================
Semantic Scholar API
====================================================

Purpose
-------
This file searches research papers using
the Semantic Scholar API.

It returns paper information like

• Title
• Abstract
• Authors
• Year
• Citation Count
"""

# ==============================================
# Import requests library.
# Used for sending HTTP requests.
# ==============================================
import requests

# ==============================================
# Base URL of Semantic Scholar API.
# ==============================================
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

# ==============================================
# Maximum number of papers.
# ==============================================
MAX_RESULTS = 5


# ==============================================
# Search Function
# ==============================================
def search_semantic_scholar(query: str):
    """
    Search research papers.

    Parameters
    ----------
    query : str
        Research topic.

    Returns
    -------
    list
        List of papers.
    """

    # ------------------------------------------
    # Parameters sent to the API.
    # ------------------------------------------
    params = {

        # User search topic.
        "query": query,

        # Number of papers.
        "limit": MAX_RESULTS,

        # Information we want.
        "fields": "title,abstract,authors,year,citationCount,url"
    }

    # ------------------------------------------
    # Send GET request.
    # ------------------------------------------
    response = requests.get(
        BASE_URL,
        params=params
    )

    # ------------------------------------------
    # Check request success.
    # ------------------------------------------
    if response.status_code != 200:
        return []

    # ------------------------------------------
    # Convert JSON into Python dictionary.
    # ------------------------------------------
    data = response.json()

    # ------------------------------------------
    # Empty list.
    # ------------------------------------------
    papers = []

    # ------------------------------------------
    # Loop through papers.
    # ------------------------------------------
    for paper in data.get("data", []):

        # Store paper information.
        papers.append({

            "title": paper.get("title"),

            "abstract": paper.get("abstract"),

            "authors": [
                author["name"]
                for author in paper.get("authors", [])
            ],

            "year": paper.get("year"),

            "citations": paper.get("citationCount"),

            "url": paper.get("url")
        })

    # ------------------------------------------
    # Return all papers.
    # ------------------------------------------
    return papers