"""
Lightweight Embeddings Module

Uses a stateless HashingVectorizer instead of TfidfVectorizer.
HashingVectorizer needs no fitting, so every text maps into the
SAME fixed vector space -- which is required for cosine similarity
comparisons (e.g. Corrective RAG relevance grading) to be meaningful.
"""

from sklearn.feature_extraction.text import HashingVectorizer

vectorizer = HashingVectorizer(
    n_features=384,
    stop_words="english",
    alternate_sign=False,
    norm=None
)


def generate_embedding(text: str):
    """
    Convert text into a 384-dim numerical vector.
    Same input always maps to the same vector space as every
    other call, unlike the previous TF-IDF implementation.
    """

    if not text or not text.strip():
        return [0.0] * 384

    vector = vectorizer.transform([text])

    return vector.toarray()[0].tolist()