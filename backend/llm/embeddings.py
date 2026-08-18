"""
Lightweight Embeddings Module

Uses TF-IDF instead of a large Hugging Face model.
This avoids downloading large models and works locally.
"""

from sklearn.feature_extraction.text import TfidfVectorizer

# Create the vectorizer once
vectorizer = TfidfVectorizer(
    max_features=384,
    stop_words="english"
)


def generate_embedding(text: str):
    """
    Convert text into a lightweight numerical vector.
    """

    if not text or not text.strip():
        return [0.0] * 384

    # Fit on the current text
    vector = vectorizer.fit_transform([text])

    result = vector.toarray()[0].tolist()

    # Make vector exactly 384 dimensions
    if len(result) < 384:
        result += [0.0] * (384 - len(result))
    else:
        result = result[:384]

    return result