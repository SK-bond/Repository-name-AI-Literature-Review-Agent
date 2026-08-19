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

def get_author_name(author):
    """
    Extract author name from different metadata formats.
    """

    if isinstance(author, str):
        return author

    if isinstance(author, dict):

        # Semantic Scholar style
        if author.get("name"):
            return author["name"]

        # arXiv/API style
        if author.get("full_name"):
            return author["full_name"]

        if author.get("first") or author.get("last"):
            return " ".join(
                filter(
                    None,
                    [
                        author.get("first"),
                        author.get("last")
                    ]
                )
            )

    return None


def get_paper_authors(paper):
    """
    Extract authors from different paper metadata formats.
    """

    authors = (
        paper.get("authors")
        or paper.get("author")
        or []
    )

    # If a single author was returned as a string
    if isinstance(authors, str):
        return authors

    # Convert author objects into names
    names = []

    for author in authors:

        name = get_author_name(author)

        if name:
            names.append(name)

    return ", ".join(names) if names else "Unknown Author"


def get_paper_year(paper):
    """
    Extract publication year from different metadata formats.
    """

    year = (
        paper.get("year")
        or paper.get("published_year")
        or paper.get("publication_year")
    )

    # Sometimes publication date is available instead
    if not year:

        published = paper.get("published")

        if published:
            try:
                year = str(published)[:4]
            except Exception:
                pass

    return str(year) if year else "Unknown Year"

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
    author_text = get_paper_authors(paper)

    year = get_paper_year(paper)

    # -----------------------------------------
    # Get URL.
    # -----------------------------------------
    url = paper.get("url") or paper.get("link") or paper.get("pdf_url") or ""

    # -----------------------------------------
    # Create APA citation.
    # -----------------------------------------
    citation = (
        f"- {author_text} ({year}). "
        f"{title}. {url}"
    )

    return citation