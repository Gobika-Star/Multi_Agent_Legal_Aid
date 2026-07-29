"""
agents/agent2_classifier.py
Agent 2 — Grievance Classifier

Classifies the normalized English query into a legal category
and returns a confidence score.
"""

from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CATEGORIES = [
    "labor",
    "land",
    "consumer",
    "family",
    "cyber",
    "police",
    "other"
]


def classify_grievance(normalized_query: str) -> dict:
    """
    Classifies query into a category AND identifies the likely applicable
    IPC/BNS section (if a specific criminal offense section applies).
    """
    system_prompt = f"""You are a legal grievance classification agent for an Indian legal aid system.

Step 1: Classify the query into EXACTLY ONE of these categories:
{", ".join(CATEGORIES)}

Category definitions:
- labor: wage non-payment, wrongful termination, workplace harassment, PF/gratuity issues
- land: property disputes, illegal construction, boundary issues, tenancy/rent, deposit disputes
- consumer: defective goods, service deficiency, refund/warranty issues, online shopping fraud
- family: divorce, maintenance, domestic violence, child custody, marriage disputes
- cyber: online fraud, phishing, cyberbullying, data/identity theft, social media harassment
- police: FIR filing issues, police inaction, custodial issues
- other: anything that doesn't clearly fit above

Step 2: If the situation clearly matches a specific criminal offense with a well-known IPC or BNS section (e.g. cheating/fraud = IPC 420 / BNS 318, rape = IPC 376 / BNS 64, theft = IPC 379 / BNS 303, criminal breach of trust = IPC 406 / BNS 316, assault on woman/outraging modesty = IPC 354 / BNS 74, dowry harassment = IPC 498A / BNS 85, murder = IPC 302 / BNS 103, defamation = IPC 499 / BNS 356), identify it. If no specific section clearly applies, return null.

Also provide a confidence score (0.0 to 1.0) and a one-line reason.

Respond ONLY in this exact JSON format, nothing else, no markdown, no backticks:
{{
  "category": "<one category from the list>",
  "confidence": <float 0.0-1.0>,
  "reason": "<one line explanation>",
  "applicable_section": "<e.g. 'IPC 420 / BNS 318 - Cheating' or null if none clearly applies>",
  "offense_summary": "<one line: what this section covers, or null>"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": normalized_query}
        ],
        temperature=0.1,
        max_tokens=300
    )

    raw_output = response.choices[0].message.content.strip()
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw_output)
        if result.get("category") not in CATEGORIES:
            result["category"] = "other"
    except json.JSONDecodeError:
        result = {
            "category": "other",
            "confidence": 0.0,
            "reason": "Failed to parse classifier output",
            "applicable_section": None,
            "offense_summary": None
        }

    return result

# Quick standalone test
if __name__ == "__main__":
    test_queries = [
        "My landlord is not returning my deposit, it has been 3 months.",
        "Someone tricked me into transferring money by pretending to be from my bank.",
        "I was sexually assaulted by a colleague at work.",
        "My office has not paid my salary for 2 months."
    ]

    for q in test_queries:
        print(f"\nInput: {q}")
        result = classify_grievance(q)
        print(f"Output: {result}")