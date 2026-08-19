import re


# -------------------------------------------------------
# Function: clean_text
# -------------------------------------------------------
def clean_text(text: str) -> str:
    """
    Clean and normalize paper summary/abstract text before
    inserting it into the generated review.

    - Removes leftover LaTeX commands (e.g. ~\\cite{...}, \\cite{...})
    - Collapses internal line breaks and extra whitespace
      into single spaces, so each summary renders as one
      clean paragraph.
    - Strips leading/trailing whitespace.
    """

    if not text:
        return ""

    # Remove LaTeX citation commands like ~\cite{...} or \cite{...}
    text = re.sub(r"~?\\cite\{[^}]*\}", "", text)

    # Remove other common stray LaTeX commands (\ref{...}, \label{...})
    text = re.sub(r"~?\\(ref|label)\{[^}]*\}", "", text)

    # Collapse all whitespace (including newlines/tabs) into single spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leftover double spaces caused by removed LaTeX commands
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()


def generate_review(
    topic: str,
    summaries: list,
    citations: list,
    research_gap: str
):

    review = f"""
# Literature Review: {topic}

## 1. Introduction

{topic} is an important research area in computer science and
artificial intelligence. Researchers have investigated different
approaches, methodologies, and applications related to this field.

This literature review presents the major findings from the
research papers retrieved for the selected topic.

---

## 2. Related Work

"""

    for i, summary in enumerate(summaries, 1):

        clean_summary = clean_text(summary)

        review += f"""### Research Paper {i}

{clean_summary}

"""

    review += """---

## 3. Key Findings

The reviewed research papers demonstrate continued development
within this research area.

The major findings include:

- Development of improved computational methods.
- Increasing application of artificial intelligence techniques.
- Improvements in accuracy and performance.
- Research into efficient and scalable approaches.
- Increasing interest in real-world applications.

---

## 4. Research Gaps

"""

    review += clean_text(research_gap)

    review += """

---

## 5. Conclusion

The reviewed literature demonstrates significant progress in the
selected research area. However, challenges remain in areas such
as scalability, computational efficiency, robustness,
generalization, and real-world implementation.

Future research can focus on addressing these limitations and
developing more reliable and efficient solutions.

---

## References

"""

    for citation in citations:

        review += f"- {citation}\n"

    return review