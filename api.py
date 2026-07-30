"""
api.py
FastAPI backend for the Vernacular Legal Aid Navigator.

Endpoints:
  POST /analyze  — run the full 6-agent pipeline
  GET  /health   — health check
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

from main import build_graph, GrievanceState
from utils.helper import get_logger

load_dotenv()
logger = get_logger(__name__)

app = FastAPI(
    title="Vernacular Legal Aid Navigator API",
    description="Multilingual AI-powered legal assistant for Indian citizens.",
    version="1.0.0",
)

# Allow React dev server (port 5173) and production builds
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compile graph once at startup — avoids re-compilation on every request
_graph = build_graph()


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class AnalyzeRequest(BaseModel):
    """Request body for the /analyze endpoint."""
    query: str = Field(..., min_length=5, max_length=2000, description="User's legal problem description")


class LawEntry(BaseModel):
    title: str
    text: str
    category: str


class ForumInfo(BaseModel):
    forum: str
    how_to_approach: str
    typical_timeline: str
    cost: str
    official_portal: str = ""
    helpline: str = ""


class ChecklistInfo(BaseModel):
    base_items: List[str]
    additional_items: List[str]
    full_checklist: List[str]


class AnalyzeResponse(BaseModel):
    """Full response from the 6-agent pipeline."""
    raw_query: str
    detected_language: str
    normalized_query: str
    category: str
    confidence: float
    laws: List[LawEntry]
    forum_info: ForumInfo
    explanation: str
    key_points: List[str]
    checklist: ChecklistInfo


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "Vernacular Legal Aid Navigator"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    """
    Run the full 6-agent legal aid pipeline on the user's query.

    Args:
        request: AnalyzeRequest with the user's problem description.

    Returns:
        AnalyzeResponse with language, category, laws, forum, explanation, and checklist.
    """
    logger.info("Received query: %s", request.query[:80])

    initial_state: GrievanceState = {
        "raw_query": request.query,
        "detected_language": "",
        "normalized_query": "",
        "category": "",
        "confidence": 0.0,
        "laws": [],
        "forum_info": {},
        "explanation": "",
        "key_points": [],
        "checklist": {},
    }

    try:
        final_state = _graph.invoke(initial_state)
    except Exception as e:
        logger.error("Pipeline error: %s", e)
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

    # Ensure checklist has all required keys
    checklist = final_state.get("checklist", {})
    if not checklist:
        checklist = {"base_items": [], "additional_items": [], "full_checklist": []}

    return AnalyzeResponse(
        raw_query=final_state["raw_query"],
        detected_language=final_state["detected_language"],
        normalized_query=final_state["normalized_query"],
        category=final_state["category"],
        confidence=final_state["confidence"],
        laws=[LawEntry(**law) for law in final_state["laws"]],
        forum_info=ForumInfo(**final_state["forum_info"]),
        explanation=final_state["explanation"],
        key_points=final_state["key_points"],
        checklist=ChecklistInfo(**checklist),
    )


# ---------------------------------------------------------------------------
# Run with: uvicorn api:app --reload --port 8000
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
