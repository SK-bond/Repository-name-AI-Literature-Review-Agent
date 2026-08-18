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

        review += f"""
### Research Paper {i}

{summary}

"""

    review += """
---

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

    review += research_gap

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