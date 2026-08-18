"""
========================================================
arXiv API Module
========================================================

Purpose:
--------
This file communicates with the arXiv API.

It sends a research topic and receives
a list of matching research papers.
"""

# -------------------------------------------------------
# Import requests library.
# It allows Python to send HTTP requests to websites/APIs.
# -------------------------------------------------------
import requests

# -------------------------------------------------------
# Import XML parser.
# arXiv returns XML data instead of JSON.
# We use ElementTree to read XML.
# -------------------------------------------------------
import xml.etree.ElementTree as ET

# -------------------------------------------------------
# Maximum papers to fetch.
# -------------------------------------------------------
MAX_RESULTS = 5


# -------------------------------------------------------
# Function to search papers
# -------------------------------------------------------
def search_arxiv(query: str):
    """
    Search research papers from arXiv.

    Parameters
    ----------
    query : str
        Research topic entered by the user.

    Returns
    -------
    list
        List of research papers.
    """

    # Base URL of arXiv API.
    base_url = "http://export.arxiv.org/api/query"

    # Parameters sent to the API.
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": MAX_RESULTS
    }

    # Send GET request.
    response = requests.get(base_url, params=params)

    # Check if request failed.
    if response.status_code != 200:
        return []

    # Parse XML response.
    root = ET.fromstring(response.text)

    # Namespace used by arXiv XML.
    namespace = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    # Store papers here.
    papers = []

    # Loop through every paper.
    for entry in root.findall("atom:entry", namespace):

        # Extract paper title.
        title = entry.find("atom:title", namespace).text.strip()

        # Extract summary.
        summary = entry.find("atom:summary", namespace).text.strip()

        # Extract paper link.
        link = entry.find("atom:id", namespace).text

        # Store paper information.
        papers.append({
            "title": title,
            "summary": summary,
            "link": link
        })

    # Return all papers.
    return papers