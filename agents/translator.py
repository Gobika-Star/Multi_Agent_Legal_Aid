from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def translate_report_to_tamil(report: dict) -> dict:
    """
    Translates the key user-facing text fields of the final report into Tamil.
    Keeps structure identical, only translates text values.
    """
    system_prompt = """You are a translation agent. Translate the given English legal report fields into clear, natural Tamil.
Keep proper nouns (like Act names, IPC/BNS section numbers, portal names, DLSA) in English/as-is, but translate all explanatory text into Tamil.
Preserve the JSON structure exactly.

Respond ONLY with valid JSON in the same structure as given, nothing else, no markdown, no backticks."""

    user_content = json.dumps(report, ensure_ascii=False)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2,
        max_tokens=3000
    )

    raw_output = response.choices[0].message.content.strip()
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        translated = json.loads(raw_output)
    except json.JSONDecodeError as e:
        print("=" * 50)
        print("TRANSLATION FAILED:", e)
        print("RAW MODEL OUTPUT WAS:")
        print(raw_output)
        print("=" * 50)
        translated = report  # fallback to English if translation fails

    return translated


def translate_examples_to_tamil(examples: dict) -> dict:
    """
    Translates a simple {label: sentence} dict of example queries into Tamil.
    Used to show example prompts in Tamil without hardcoding translations.
    """
    system_prompt = """Translate the given English phrases into natural, conversational Tamil.
Input is a JSON object where each key is a short label and each value is a sentence.
Translate BOTH the keys and values into Tamil.

Respond ONLY with valid JSON in the same structure (translated keys and values), nothing else, no markdown, no backticks."""

    user_content = json.dumps(examples, ensure_ascii=False)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2,
        max_tokens=1000
    )

    raw_output = response.choices[0].message.content.strip()
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        translated = json.loads(raw_output)
    except json.JSONDecodeError:
        translated = examples  # fallback to English if translation fails

    return translated


if __name__ == "__main__":
    sample_report = {
        "explanation": "The law protects you from fraud. You can file a complaint.",
        "key_points": ["Cheating is a criminal offense.", "You can report it to police."],
        "steps_to_overcome": ["File an FIR immediately.", "Collect all transaction proof."]
    }
    result = translate_report_to_tamil(sample_report)
    print(json.dumps(result, ensure_ascii=False, indent=2))