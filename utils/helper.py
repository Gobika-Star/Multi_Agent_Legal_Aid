"""
utils/helper.py
Shared utility functions used across all agents.
"""

import json
import logging
import os
import re
from typing import Any

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """Return a consistently configured logger for the given module name."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


# ---------------------------------------------------------------------------
# Groq client
# ---------------------------------------------------------------------------

def get_groq_client() -> Groq:
    """Create and return a Groq client using the API key from environment."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is not set in the environment.")
    return Groq(api_key=api_key)


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------

def parse_llm_json(raw_output: str, fallback: dict) -> dict:
    """
    Safely parse JSON from LLM output.

    Strips markdown fences if present, then attempts json.loads.
    Returns `fallback` dict on any parse failure.

    Args:
        raw_output: Raw string from LLM response.
        fallback: Dict to return if parsing fails.

    Returns:
        Parsed dict or fallback dict.
    """
    # Strip markdown code fences
    cleaned = re.sub(r"```(?:json)?", "", raw_output).replace("```", "").strip()

    # Extract first JSON object if there's surrounding text
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger = get_logger(__name__)
        logger.warning("JSON parse failed. Raw output: %s", raw_output[:200])
        return fallback


# ---------------------------------------------------------------------------
# Groq chat helper
# ---------------------------------------------------------------------------

def groq_chat(
    client: Groq,
    system_prompt: str,
    user_content: str,
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.2,
    max_tokens: int = 400,
) -> str:
    """
    Send a chat completion request to Groq and return the response text.

    Args:
        client: Groq client instance.
        system_prompt: System role instructions.
        user_content: User message content.
        model: Groq model identifier.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens in response.

    Returns:
        Stripped response string from the LLM.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
