"""
scraper/scrape_bsa.py
Scraper for Bharatiya Sakshya Adhiniyam (BSA), 2023.

Saves structured JSON to knowledge_base/bsa_sections.json.

Run: python scraper/scrape_bsa.py
"""

import json
import os
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "knowledge_base", "bsa_sections.json")

FALLBACK_SECTIONS = [
    {
        "id": "bsa_s2",
        "act": "BSA",
        "section": "2(1)(c)",
        "title": "Definition of Document",
        "text": "Document includes any matter expressed or described upon any substance by means of letters, figures or marks, or by more than one of those means, intended to be used, or which may be used, for the purpose of recording that matter. Electronic records are explicitly included.",
        "category": "police",
    },
    {
        "id": "bsa_s57",
        "act": "BSA",
        "section": "57",
        "title": "Admissibility of electronic records",
        "text": "Any information contained in an electronic record which is printed on a paper, stored, recorded or copied in optical or magnetic media produced by a computer shall be deemed to be also a document and shall be admissible in any proceedings, without further proof or production of the original, if the conditions in Section 63 are satisfied.",
        "category": "cyber",
    },
    {
        "id": "bsa_s63",
        "act": "BSA",
        "section": "63",
        "title": "Certificate for electronic evidence",
        "text": "A certificate identifying the electronic record, describing the manner of its production, giving the particulars of the device involved, and signed by a person occupying a responsible official position, shall be evidence of any matter stated in the certificate. This makes WhatsApp messages, emails, and screenshots admissible in court.",
        "category": "cyber",
    },
    {
        "id": "bsa_s23",
        "act": "BSA",
        "section": "23",
        "title": "Admissions by party to proceedings",
        "text": "An admission is a statement, oral or documentary or contained in electronic form, which suggests any inference as to any fact in issue or relevant fact, and which is made by any of the persons and under the circumstances specified in this Chapter.",
        "category": "police",
    },
    {
        "id": "bsa_s39",
        "act": "BSA",
        "section": "39",
        "title": "Relevancy of statements in maps, charts and plans",
        "text": "Statements of facts in issue or relevant facts, made in published maps or charts generally offered for public sale, or in maps or plans made under the authority of the Central Government or any State Government, as to matters usually represented or stated in such maps, charts or plans, are themselves relevant facts.",
        "category": "land",
    },
    {
        "id": "bsa_s116",
        "act": "BSA",
        "section": "116",
        "title": "Burden of proof in cases of dowry death",
        "text": "When the question is whether a person has committed the dowry death of a woman, and it is shown that soon before her death such woman had been subjected by such person to cruelty or harassment for, or in connection with, any demand for dowry, the court shall presume that such person had caused the dowry death.",
        "category": "family",
    },
]


def scrape_bsa() -> list:
    """
    Return curated BSA sections (scraping not feasible for PDF-only sources).

    Returns:
        List of section dicts.
    """
    logger.info("Using %d curated BSA sections.", len(FALLBACK_SECTIONS))
    return FALLBACK_SECTIONS


def main():
    """Save BSA sections to knowledge_base/bsa_sections.json."""
    sections = scrape_bsa()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)

    logger.info("Saved %d BSA sections to %s", len(sections), OUTPUT_PATH)


if __name__ == "__main__":
    main()
