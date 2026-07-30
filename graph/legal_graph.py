"""
graph/legal_graph.py
LangGraph workflow for the Vernacular Legal Aid Navigator.

Workflow:
  normalize → classify → [retrieve_laws + locate_forum in parallel] → explain → checklist

Agents 3 and 4 run in parallel using LangGraph's fan-out/fan-in pattern.
"""

from typing import TypedDict, List, Annotated
import operator

from langgraph.graph import StateGraph, END

from agents.agent1_normalizer import normalize_query
from agents.agent2_classifier import classify_grievance
from agents.agent3_law_retriever import retrieve_laws
from agents.agent4_forum_locator import locate_forum
from agents.agent5_explainer import explain_laws
from agents.agent6_checklist import generate_checklist
from utils.helper import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Shared state schema
# ---------------------------------------------------------------------------

class GrievanceState(TypedDict):
    """Shared state passed between all agents in the graph."""
    raw_query: str
    detected_language: str
    normalized_query: str
    category: str
    confidence: float
    laws: List[dict]
    forum_info: dict
    explanation: str
    key_points: List[str]
    checklist: dict


# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------

def node_normalize(state: GrievanceState) -> dict:
    """Agent 1: Detect language and normalize query to English."""
    logger.info("[Agent 1] Normalizing...")
    result = normalize_query(state["raw_query"])
    return {
        "detected_language": result["detected_language"],
        "normalized_query": result["normalized_query"],
    }


def node_classify(state: GrievanceState) -> dict:
    """Agent 2: Classify the normalized query into a legal category."""
    logger.info("[Agent 2] Classifying...")
    result = classify_grievance(state["normalized_query"])
    return {
        "category": result["category"],
        "confidence": result["confidence"],
    }


def node_retrieve_laws(state: GrievanceState) -> dict:
    """Agent 3: Retrieve relevant laws via RAG."""
    logger.info("[Agent 3] Retrieving laws...")
    laws = retrieve_laws(state["normalized_query"], state["category"])
    return {"laws": laws}


def node_locate_forum(state: GrievanceState) -> dict:
    """Agent 4: Locate the appropriate legal forum."""
    logger.info("[Agent 4] Locating forum...")
    forum_info = locate_forum(state["category"])
    return {"forum_info": forum_info}


def node_explain(state: GrievanceState) -> dict:
    """Agent 5: Generate plain-language explanation."""
    logger.info("[Agent 5] Explaining...")
    result = explain_laws(state["normalized_query"], state["laws"])
    return {
        "explanation": result["explanation"],
        "key_points": result["key_points"],
    }


def node_checklist(state: GrievanceState) -> dict:
    """Agent 6: Generate document checklist."""
    logger.info("[Agent 6] Generating checklist...")
    result = generate_checklist(state["normalized_query"], state["category"])
    return {"checklist": result}


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def build_graph():
    """
    Build and compile the LangGraph workflow.

    Agents 3 and 4 run in parallel after classification.
    Agent 5 waits for both to complete before explaining.

    Returns:
        Compiled LangGraph application.
    """
    graph = StateGraph(GrievanceState)

    # Register nodes
    graph.add_node("normalize", node_normalize)
    graph.add_node("classify", node_classify)
    graph.add_node("retrieve_laws", node_retrieve_laws)
    graph.add_node("locate_forum", node_locate_forum)
    graph.add_node("explain", node_explain)
    graph.add_node("checklist", node_checklist)

    # Sequential flow
    graph.set_entry_point("normalize")
    graph.add_edge("normalize", "classify")

    # Parallel fan-out: classify → both retrieve_laws AND locate_forum
    graph.add_edge("classify", "retrieve_laws")
    graph.add_edge("classify", "locate_forum")

    # Fan-in: both parallel nodes → explain
    graph.add_edge("retrieve_laws", "explain")
    graph.add_edge("locate_forum", "explain")

    graph.add_edge("explain", "checklist")
    graph.add_edge("checklist", END)

    return graph.compile()
