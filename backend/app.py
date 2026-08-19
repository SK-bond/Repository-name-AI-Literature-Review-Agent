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
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    # Your Vercel frontend
    allow_origins=[
        "https://ai-literature-review-agent.vercel.app"
    ],

    # No login/cookies are being used
    allow_credentials=False,

    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Request Model
# =========================================================

class ReviewRequest(BaseModel):

    topic: str


# =========================================================
# Home
# =========================================================

@app.get("/")
def home():

    return {
        "message": "AI Literature Review Agent Backend Running"
    }


# =========================================================
# Review
# =========================================================

@app.post("/review")
def review(request: ReviewRequest):

    print()
    print("=" * 60)
    print("REQUEST RECEIVED")
    print("Topic:", request.topic)
    print("=" * 60)

    result = run_literature_review(request.topic)

    return {
        "topic": request.topic,
        "review": result
    }