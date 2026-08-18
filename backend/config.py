"""
=========================================
Configuration File
=========================================

Purpose:
--------
This file loads all configuration values
(API keys, model names, folder paths, etc.)
from one central location.

Benefits:
---------
1. Keeps secrets out of the code.
2. Easy to update configuration.
3. Cleaner project structure.
"""

# Import os so we can read environment variables.
import os

# Import load_dotenv.
# This reads the .env file automatically.
from dotenv import load_dotenv

# Load all variables from the .env file.
load_dotenv()

# ======================================================
# OpenAI Configuration
# ======================================================

# Read the OpenAI API key from the .env file.
# If the key doesn't exist, this returns None.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ======================================================
# Semantic Scholar Configuration
# ======================================================

# Read the Semantic Scholar API key.
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

# ======================================================
# Application Settings
# ======================================================

# Name of the embedding model.
# This model converts text into vectors.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Name of the OpenAI model we will use.
LLM_MODEL = "google/flan-t5-base"

# Folder where reports will be saved.
REPORT_FOLDER = "reports"

# Folder used to store cached files.
DATA_FOLDER = "data"

# Name of the ChromaDB collection.
CHROMA_COLLECTION = "research_papers"

# Maximum number of papers to fetch.
MAX_PAPERS = 10