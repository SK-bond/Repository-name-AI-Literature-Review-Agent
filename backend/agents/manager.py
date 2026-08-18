"""
AI Literature Review Manager
"""

from backend.agents.search_agent import search_papers
from backend.agents.summary_agent import summarize_paper
from backend.agents.citation_agent import generate_citation
from backend.agents.gap_agent import identify_research_gap
from backend.agents.review_agent import generate_review


def run_literature_review(topic: str):

    print("=" * 60)
    print("AI Literature Review Agent Started")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1: SEARCH
    # --------------------------------------------------

    print("Searching research papers...")

    papers = search_papers(topic)

    print(f"Found {len(papers)} research papers.")

    if not papers:

        return "No research papers were found for this topic."

    # --------------------------------------------------
    # STEP 2: SUMMARIZE
    # --------------------------------------------------

    print("Starting paper summarization...")

    summaries = []

    for i, paper in enumerate(papers, 1):

        print(f"Summarizing paper {i}/{len(papers)}...")

        text = (
            paper.get("summary")
            or paper.get("abstract")
            or paper.get("title")
            or ""
        )

        summary = summarize_paper(text)

        summaries.append(summary)

    print("Paper summaries completed.")

    # --------------------------------------------------
    # STEP 3: CITATIONS
    # --------------------------------------------------

    print("Generating citations...")

    citations = []

    for paper in papers:

        citation = generate_citation(paper)

        citations.append(citation)

    print("Citations generated.")

    # --------------------------------------------------
    # STEP 4: RESEARCH GAP
    # --------------------------------------------------

    print("Identifying research gaps...")

    research_gap = identify_research_gap(summaries)

    print("Research gap identified.")

    # --------------------------------------------------
    # STEP 5: FINAL REVIEW
    # --------------------------------------------------

    print("Generating final literature review...")

    review = generate_review(
        topic=topic,
        summaries=summaries,
        citations=citations,
        research_gap=research_gap
    )

    print("Literature review completed.")

    return review