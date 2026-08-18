# 📚 AI Literature Review Agent

## Overview

AI Literature Review Agent is an AI-powered application that automatically searches research papers, summarizes them, identifies research gaps, generates citations, and produces a complete literature review.

---

## Features

- Search papers from arXiv
- Search papers from Semantic Scholar
- Generate AI summaries
- Generate APA citations
- Identify research gaps
- Produce complete literature reviews
- Streamlit Web Interface
- FastAPI Backend

---

## Technologies Used

- Python
- FastAPI
- Streamlit
- OpenAI API
- ChromaDB
- Sentence Transformers
- arXiv API
- Semantic Scholar API

---

## Project Structure

AI_Literature_Review_Agent/

backend/

frontend/

reports/

requirements.txt

README.md

---

## Installation

```bash
git clone <repository>

cd AI_Literature_Review_Agent

pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn backend.app:app --reload
```

---

## Run Frontend

```bash
streamlit run frontend/app.py
```

---

## Future Improvements

- PDF export
- Multi-agent workflow
- Local LLM support
- RAG implementation
- Multi-language support

---

## Author

Sheevamraj Singh