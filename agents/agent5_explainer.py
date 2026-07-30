from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def explain_laws(normalized_query: str, laws: list, applicable_section: str = None, offense_summary: str = None) -> dict:
    """
    Takes the user's situation + retrieved law excerpts (from Agent 3) + applicable
    IPC/BNS section (from Agent 2) and produces:
    1. A plain-language explanation
    2. Key points
    3. Concrete step-by-step action plan to overcome the problem
    """
    if not laws and not applicable_section:
        return {
            "explanation": "We couldn't find specific matching laws for this situation. Please consult your nearest District Legal Services Authority (DLSA) for free guidance.",
            "key_points": [],
            "steps_to_overcome": [
                "Visit or call your nearest District Legal Services Authority (DLSA) for free legal advice.",
                "Write down all details of your situation with dates before you go."
            ]
        }

    laws_text = "\n\n".join([f"- {law['title']}: {law['text']}" for law in laws]) if laws else "None retrieved"
    section_text = f"Applicable section: {applicable_section} ({offense_summary})" if applicable_section else "No specific criminal section identified"

    system_prompt = """You are a legal explainer and action-planning agent for an Indian legal aid system serving citizens with no legal background.

Given the user's situation, relevant law excerpts, and applicable IPC/BNS section (if any), provide:
1. A simple plain-language explanation (2-3 sentences) of what the law says
2. 2-4 key points in plain language
3. A concrete STEP-BY-STEP action plan (3-6 steps) telling the person exactly what to do, in order, to address their problem

Rules:
- No legal jargon
- Steps must be practical and actionable, in the correct order
- Do NOT invent facts not present in the law excerpts
- Be specific to their situation, not generic

Respond ONLY in this exact JSON format, nothing else, no markdown, no backticks:
{
  "explanation": "<2-3 sentence plain language summary>",
  "key_points": ["<point 1>", "<point 2>", "<point 3>"],
  "steps_to_overcome": ["<step 1>", "<step 2>", "<step 3>", "<step 4>"]
}
"""

    user_content = f"User's situation: {normalized_query}\n\n{section_text}\n\nRelevant laws:\n{laws_text}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.3,
        max_tokens=600
    )

    raw_output = response.choices[0].message.content.strip()
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw_output)
    except json.JSONDecodeError:
        result = {
            "explanation": "We found relevant laws but couldn't generate a simplified summary. Please review the raw law excerpts above.",
            "key_points": [],
            "steps_to_overcome": []
        }

    return result


if __name__ == "__main__":
    from agent3_law_retriever import retrieve_laws

    test_query = "Someone tricked me into transferring money by pretending to be from my bank."
    test_category = "cyber"
    test_section = "IPC 420 / BNS 318 - Cheating"
    test_summary = "Deceiving someone to gain money or property dishonestly"

    laws = retrieve_laws(test_query, test_category)
    print("Retrieved laws:", [l["title"] for l in laws])

    result = explain_laws(test_query, laws, test_section, test_summary)
    print("\nExplanation:", result["explanation"])
    print("\nKey points:")
    for point in result["key_points"]:
        print(f"  - {point}")
    print("\nSteps to overcome:")
    for i, step in enumerate(result["steps_to_overcome"], 1):
        print(f"  {i}. {step}")