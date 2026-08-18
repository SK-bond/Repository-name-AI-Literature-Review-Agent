from fastapi import FastAPI
from pydantic import BaseModel

from backend.agents.manager import run_literature_review


app = FastAPI(
    title="AI Literature Review Agent",
    version="1.0.0"
)


class ReviewRequest(BaseModel):

    topic: str


@app.get("/")
def home():

    return {
        "message": "AI Literature Review Agent Backend Running"
    }


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