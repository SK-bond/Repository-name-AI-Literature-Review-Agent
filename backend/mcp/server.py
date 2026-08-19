"""
=========================================================
MCP Server: Literature Review Tools
=========================================================

Exposes each agent as an MCP tool, so the manager orchestrates
the pipeline through the Model Context Protocol instead of
calling agent functions directly.
"""

from mcp.server.fastmcp import FastMCP

from backend.agents.search_agent import search_papers
from backend.agents.summary_agent import summarize_paper
from backend.agents.citation_agent import generate_citation
from backend.agents.gap_agent import identify_research_gap
from backend.agents.review_agent import generate_review

mcp = FastMCP("literature-review")


@mcp.tool()
def search(topic: str) -> list:
    """Search arXiv + Semantic Scholar for a topic, apply Corrective
    RAG relevance grading, store results in ChromaDB, and return them."""
    return search_papers(topic)


@mcp.tool()
def summarize(text: str) -> str:
    """Summarize a paper's abstract/summary text."""
    return summarize_paper(text)


@mcp.tool()
def cite(paper: dict) -> str:
    """Generate an APA-style citation for a paper."""
    return generate_citation(paper)


@mcp.tool()
def find_research_gap(summaries: list) -> str:
    """Identify research gaps across a list of paper summaries."""
    return identify_research_gap(summaries)


@mcp.tool()
def build_review(
    topic: str,
    summaries: list,
    citations: list,
    research_gap: str
) -> str:
    """Assemble the final literature review document."""
    return generate_review(topic, summaries, citations, research_gap)


if __name__ == "__main__":
    mcp.run(transport="stdio")