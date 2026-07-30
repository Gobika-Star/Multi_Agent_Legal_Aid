from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
from dotenv import load_dotenv

from agents.agent1_normalizer import normalize_query
from agents.agent2_classifier import classify_grievance
from agents.agent3_law_retriever import retrieve_laws
from agents.agent4_forum_locator import locate_forum
from agents.agent5_explainer import explain_laws
from agents.agent6_checklist import generate_checklist

load_dotenv()


class GrievanceState(TypedDict):
    raw_query: str
    detected_language: str
    normalized_query: str
    category: str
    confidence: float
    applicable_section: Optional[str]
    offense_summary: Optional[str]
    laws: List[dict]
    forum_info: dict
    explanation: str
    key_points: List[str]
    steps_to_overcome: List[str]
    checklist: dict


def node_normalize(state: GrievanceState) -> GrievanceState:
    result = normalize_query(state["raw_query"])
    state["detected_language"] = result["detected_language"]
    state["normalized_query"] = result["normalized_query"]
    return state


def node_classify(state: GrievanceState) -> GrievanceState:
    result = classify_grievance(state["normalized_query"])
    state["category"] = result["category"]
    state["confidence"] = result["confidence"]
    state["applicable_section"] = result.get("applicable_section")
    state["offense_summary"] = result.get("offense_summary")
    return state


def node_retrieve_laws(state: GrievanceState) -> GrievanceState:
    laws = retrieve_laws(state["normalized_query"], state["category"])
    state["laws"] = laws
    return state


def node_locate_forum(state: GrievanceState) -> GrievanceState:
    forum_info = locate_forum(state["category"])
    state["forum_info"] = forum_info
    return state


def node_explain(state: GrievanceState) -> GrievanceState:
    result = explain_laws(
        state["normalized_query"],
        state["laws"],
        state.get("applicable_section"),
        state.get("offense_summary")
    )
    state["explanation"] = result["explanation"]
    state["key_points"] = result["key_points"]
    state["steps_to_overcome"] = result.get("steps_to_overcome", [])
    return state


def node_checklist(state: GrievanceState) -> GrievanceState:
    result = generate_checklist(state["normalized_query"], state["category"])
    state["checklist"] = result
    return state


def build_graph():
    graph = StateGraph(GrievanceState)

    graph.add_node("normalize", node_normalize)
    graph.add_node("classify", node_classify)
    graph.add_node("retrieve_laws", node_retrieve_laws)
    graph.add_node("locate_forum", node_locate_forum)
    graph.add_node("explain", node_explain)
    graph.add_node("checklist", node_checklist)

    graph.set_entry_point("normalize")
    graph.add_edge("normalize", "classify")
    graph.add_edge("classify", "retrieve_laws")
    graph.add_edge("retrieve_laws", "locate_forum")
    graph.add_edge("locate_forum", "explain")
    graph.add_edge("explain", "checklist")
    graph.add_edge("checklist", END)

    return graph.compile()


def run_pipeline(raw_query: str) -> GrievanceState:
    app = build_graph()
    initial_state: GrievanceState = {
        "raw_query": raw_query,
        "detected_language": "",
        "normalized_query": "",
        "category": "",
        "confidence": 0.0,
        "applicable_section": None,
        "offense_summary": None,
        "laws": [],
        "forum_info": {},
        "explanation": "",
        "key_points": [],
        "steps_to_overcome": [],
        "checklist": {}
    }
    final_state = app.invoke(initial_state)
    return final_state


if __name__ == "__main__":
    test_query = "Someone tricked me into transferring money by pretending to be from my bank."
    result = run_pipeline(test_query)

    print("=" * 60)
    print(f"CATEGORY: {result['category']} | SECTION: {result['applicable_section']}")
    print(f"EXPLANATION: {result['explanation']}")
    print("\nSTEPS TO OVERCOME:")
    for i, step in enumerate(result["steps_to_overcome"], 1):
        print(f"  {i}. {step}")
    print("=" * 60)