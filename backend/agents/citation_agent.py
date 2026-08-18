"""
=========================================================
Citation Agent
=========================================================

Purpose
-------
Generate APA-style citations for research papers.
"""


# -------------------------------------------------------
# Function: generate_citation
# -------------------------------------------------------
def generate_citation(paper: dict):
    """
    Generate an APA-style citation.

    Parameters
    ----------
    paper : dict
        Dictionary containing paper details.

    Returns
    -------
    str
        APA citation.
    """

    # -----------------------------------------
    # Get title.
    # If missing, use "Unknown Title".
    # -----------------------------------------
    title = paper.get("title", "Unknown Title")

    # -----------------------------------------
    # Get year.
    # -----------------------------------------
    year = paper.get("year", "Unknown Year")

    # -----------------------------------------
    # Get authors list.
    # -----------------------------------------
    authors = paper.get("authors", [])

    # -----------------------------------------
    # Convert authors list into text.
    # -----------------------------------------
    if authors:
        author_text = ", ".join(authors)
    else:
        author_text = "Unknown Author"

    # -----------------------------------------
    # Get URL.
    # -----------------------------------------
    url = paper.get("url") or paper.get("link") or ""

    # -----------------------------------------
    # Create APA citation.
    # -----------------------------------------
    citation = (
        f"{author_text} "
        f"({year}). "
        f"{title}. "
        f"{url}"
    )

    return citation