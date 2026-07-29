"""
agents/agent1_normalizer.py
Agent 1 — Language Normalizer

Detects the language of the raw user query and translates/normalizes it
into clean English, preserving all factual details.
"""

import logging
from utils.helper import get_groq_client, groq_chat, parse_llm_json, get_logger
from utils.prompts import NORMALIZER_SYSTEM_PROMPT

logger = get_logger(__name__)

_client = get_groq_client()


def normalize_query(raw_query: str) -> dict:
    """
    Detect language and normalize the raw user query into clean English.

    Args:
        raw_query: User's input in any language or mixed language.

    Returns:
        Dict with keys 'detected_language' and 'normalized_query'.
    """
    logger.info("Normalizing query: %s", raw_query[:80])

    raw_output = groq_chat(
        client=_client,
        system_prompt=NORMALIZER_SYSTEM_PROMPT,
        user_content=raw_query,
        temperature=0.2,
        max_tokens=300,
    )

    result = parse_llm_json(
        raw_output,
        fallback={"detected_language": "unknown", "normalized_query": raw_query},
    )

    logger.info("Detected language: %s", result.get("detected_language"))
    return result


# Quick standalone test
if __name__ == "__main__":
    test_queries = [
        "Sir mera landlord deposit wapas nahi de raha, 3 mahine ho gaye",
        "என் அலுவலகத்தில் எனக்கு சம்பளம் தரவில்லை",
        "my neighbour built wall on my land what to do",
    ]
    for q in test_queries:
        print(f"\nInput: {q}")
        print(f"Output: {normalize_query(q)}")
