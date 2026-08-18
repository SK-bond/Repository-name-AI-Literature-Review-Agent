"""
Lightweight Summary Agent
"""

def summarize_paper(text: str):

    if not text or not text.strip():
        return "No content available."

    # Clean text
    text = " ".join(text.split())

    # Split into sentences
    sentences = text.split(". ")

    # Keep the first few meaningful sentences
    selected = sentences[:4]

    summary = ". ".join(selected)

    if not summary.endswith("."):
        summary += "."

    return summary