"""
agents/agent6_checklist.py
Agent 6 — Document Checklist Generator

Returns a base checklist for the legal category, then uses the LLM
to add 0-2 situation-specific items not already in the base list.
"""

from utils.helper import get_groq_client, groq_chat, parse_llm_json, get_logger
from utils.prompts import CHECKLIST_REFINEMENT_PROMPT

logger = get_logger(__name__)

_client = get_groq_client()

BASE_CHECKLIST: dict = {
    "labor": [
        "Employment offer letter / appointment letter",
        "Salary slips (last 6 months, if available)",
        "ID proof (Aadhaar / PAN)",
        "Bank statement showing salary credits",
        "Any written communication with employer (emails, termination letter, etc.)",
        "PF account number / UAN (if PF-related)",
    ],
    "land": [
        "Rent agreement / lease deed (if applicable)",
        "Property title documents / sale deed",
        "Deposit receipt or payment proof",
        "ID proof (Aadhaar / PAN)",
        "Any written communication with landlord / other party",
        "Photographs of property / damage (if relevant)",
    ],
    "consumer": [
        "Purchase invoice / receipt",
        "Product / service warranty card (if any)",
        "Screenshots of order / transaction (for online purchases)",
        "Any communication with seller about the complaint",
        "ID proof (Aadhaar / PAN)",
        "Delivery receipt or courier tracking details",
    ],
    "family": [
        "Marriage certificate",
        "ID proof (Aadhaar / PAN)",
        "Income proof of both spouses (if available)",
        "Any prior court orders (if applicable)",
        "Evidence of communication / incidents (e.g. for DV cases)",
        "Birth certificates of children (if custody-related)",
    ],
    "cyber": [
        "Screenshots of the fraud / harassment (messages, transactions, profiles)",
        "Transaction ID / bank statement (for financial fraud)",
        "ID proof (Aadhaar / PAN)",
        "Mobile number / email used in the incident",
        "Any communication with the fraudster or platform support",
        "Complaint acknowledgement from cybercrime.gov.in (if already filed)",
    ],
    "police": [
        "ID proof (Aadhaar / PAN)",
        "Written account of the incident with date, time, location",
        "Any evidence (photos, videos, witness names and contact details)",
        "Copy of any prior complaint (if this is a follow-up / escalation)",
        "Medical certificate (if physical injury involved)",
    ],
    "other": [
        "ID proof (Aadhaar / PAN)",
        "Any documents related to your issue",
        "Written summary of your situation with dates and amounts",
    ],
}


def generate_checklist(normalized_query: str, category: str) -> dict:
    """
    Generate a document checklist for the user's legal situation.

    Starts with a rule-based base checklist for the category, then
    uses the LLM to add 0-2 situation-specific items.

    Args:
        normalized_query: Clean English description of the user's problem.
        category: Legal category from Agent 2.

    Returns:
        Dict with keys 'base_items', 'additional_items', and 'full_checklist'.
    """
    base_items = BASE_CHECKLIST.get(category, BASE_CHECKLIST["other"])

    user_content = (
        f"User's situation: {normalized_query}\n\n"
        f"Base checklist already includes: {', '.join(base_items)}"
    )

    logger.info("Generating checklist for category '%s'.", category)

    try:
        raw_output = groq_chat(
            client=_client,
            system_prompt=CHECKLIST_REFINEMENT_PROMPT,
            user_content=user_content,
            temperature=0.3,
            max_tokens=150,
        )
        result = parse_llm_json(raw_output, fallback={"additional_items": []})
        additional_items = result.get("additional_items", [])
    except Exception as e:
        logger.error("Checklist refinement failed: %s", e)
        additional_items = []

    logger.info(
        "Checklist: %d base + %d additional items.",
        len(base_items),
        len(additional_items),
    )

    return {
        "base_items": base_items,
        "additional_items": additional_items,
        "full_checklist": base_items + additional_items,
    }


# Quick standalone test
if __name__ == "__main__":
    test_query = "My landlord is not returning my deposit, it has been 3 months, and there was water damage he's blaming me for."
    result = generate_checklist(test_query, "land")
    print("Full checklist:")
    for item in result["full_checklist"]:
        print(f"  - {item}")
