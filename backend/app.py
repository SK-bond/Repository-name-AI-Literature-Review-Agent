from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agents.manager import run_literature_review


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="AI Literature Review Agent",
    version="1.0.0"
)


# =========================================================
# CORS Configuration
# =========================================================
# Allows your Vercel frontend to communicate with
# the Render backend.
#
# "*" allows requests from any frontend.
# This is suitable for your hackathon/demo deployment.
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Request Model
# =========================================================

class ReviewRequest(BaseModel):

    topic: str


# =========================================================
# Home Endpoint
# =========================================================

@app.get("/")
def home():

    return {
        "message": "AI Literature Review Agent Backend Running"
    }


# =========================================================
# Literature Review Endpoint
# =========================================================

@app.post("/review")
def review(request: ReviewRequest):

    print()
    print("=" * 60)
    print("REQUEST RECEIVED")
    print("Topic:", request.topic)
    print("=" * 60)

    # Run the complete AI literature review pipeline
    result = run_literature_review(request.topic)

    return {
        "topic": request.topic,
        "review": result
    }