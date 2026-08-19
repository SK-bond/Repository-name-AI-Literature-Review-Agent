"""
=========================================================
Corrective RAG Agent
=========================================================

Purpose
-------
Grade retrieved papers for relevance to the research topic using
embedding similarity. If too few papers grade as relevant, rewrite
the query with an LLM and trigger a corrective re-search.
"""

import numpy as np
from openai import OpenAI

from backend.config import OPENAI_API_KEY
from backend.llm.embeddings import generate_embedding

client = OpenAI(api_key=OPENAI_API_KEY)

# Cosine similarity thresholds. Tune these against your own data --
# HashingVectorizer similarity scores tend to run lower than dense
# embedding models, so don't reuse thresholds from e.g. OpenAI embeddings.
RELEVANT_THRESHOLD = 0.15
IRRELEVANT_THRESHOLD = 0.05


def _cosine_similarity(a: list, b: list) -> float:

    a = np.array(a)
    b = np.array(b)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(a, b) / (norm_a * norm_b))


def grade_paper(topic_embedding: list, paper: dict) -> str:
    """
    Grade one paper's relevance to the topic.
    Returns "relevant", "ambiguous", or "irrelevant".
    """

    text = (
        paper.get("summary")
        or paper.get("abstract")
        or paper.get("title")
        or ""
    )

    paper_embedding = generate_embedding(text)

    score = _cosine_similarity(topic_embedding, paper_embedding)

    if score >= RELEVANT_THRESHOLD:
        return "relevant"

    if score <= IRRELEVANT_THRESHOLD:
        return "irrelevant"

    return "ambiguous"


def rewrite_query(topic: str) -> str:
    """
    Ask the LLM to rewrite a weak search query into a more
    effective academic search query.
    """

    prompt = (
        "The following academic search query returned mostly irrelevant "
        f"results.\n\nOriginal query: {topic}\n\n"
        "Rewrite it as a more specific, effective academic search query. "
        "Respond with ONLY the rewritten query, nothing else."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Query rewrite failed: {e}")
        return topic


def grade_and_correct(
    topic: str,
    papers: list,
    research_fn,
    min_relevant_ratio: float = 0.4
):
    """
    Corrective RAG loop.

    1. Embed the topic once.
    2. Grade every retrieved paper against it.
    3. Keep "relevant" + "ambiguous" papers, drop "irrelevant" ones.
    4. If the surviving fraction is below `min_relevant_ratio`,
       rewrite the query and re-run `research_fn` once, merging in
       any newly-found relevant papers (deduplicated by title).

    Parameters
    ----------
    topic : str
        Original search query/topic.
    papers : list
        Papers already retrieved.
    research_fn : callable
        Function taking a query string, returning a list of paper dicts.
        Used for the corrective re-search.
    """

    topic_embedding = generate_embedding(topic)

    if not papers:
        new_query = rewrite_query(topic)
        print(f"No papers found. Retrying with rewritten query: {new_query}")
        return research_fn(new_query)

    graded = [(p, grade_paper(topic_embedding, p)) for p in papers]
    kept = [p for p, g in graded if g in ("relevant", "ambiguous")]

    relevant_ratio = len(kept) / len(papers)
    print(
        f"CRAG: {len(kept)}/{len(papers)} papers passed relevance "
        f"grading ({relevant_ratio:.0%})."
    )

    if relevant_ratio >= min_relevant_ratio:
        return kept

    # -------------------------------------------------
    # Corrective action.
    # -------------------------------------------------
    new_query = rewrite_query(topic)
    print(f"Relevance too low. Corrective re-search with: {new_query}")

    new_papers = research_fn(new_query)
    new_topic_embedding = generate_embedding(new_query)

    new_graded = [
        (p, grade_paper(new_topic_embedding, p)) for p in new_papers
    ]
    new_kept = [p for p, g in new_graded if g in ("relevant", "ambiguous")]

    seen_titles = {p.get("title") for p in kept}

    for paper in new_kept:
        if paper.get("title") not in seen_titles:
            kept.append(paper)
            seen_titles.add(paper.get("title"))

    print(f"CRAG: {len(kept)} papers kept after correction.")

    return kept