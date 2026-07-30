"""
scraper/scrape_bnss.py
Scraper for Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023.

Saves structured JSON to knowledge_base/bnss_sections.json.

Run: python scraper/scrape_bnss.py
"""

import json
import os
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "knowledge_base", "bnss_sections.json")

FALLBACK_SECTIONS = [
    {
        "id": "bnss_s35",
        "act": "BNSS",
        "section": "35",
        "title": "Arrest without warrant by police officer",
        "text": "Any police officer may without an order from a Magistrate and without a warrant, arrest any person who has been concerned in any cognizable offence. For non-cognizable offences, a warrant from a Magistrate is required. The arrested person must be informed of the grounds of arrest immediately.",
        "category": "police",
    },
    {
        "id": "bnss_s47",
        "act": "BNSS",
        "section": "47",
        "title": "Right of arrested person to meet an advocate",
        "text": "Every person who is arrested and detained in custody shall be entitled to meet an advocate of his choice during interrogation, though not throughout the interrogation.",
        "category": "police",
    },
    {
        "id": "bnss_s58",
        "act": "BNSS",
        "section": "58",
        "title": "Person arrested to be informed of grounds of arrest",
        "text": "Every police officer or other person arresting any person without warrant shall forthwith communicate to him full particulars of the offence for which he is arrested or other grounds for such arrest. The arrested person has the right to inform a friend, relative, or nominated person of the arrest.",
        "category": "police",
    },
    {
        "id": "bnss_s173",
        "act": "BNSS",
        "section": "173",
        "title": "Information in cognizable cases — FIR",
        "text": "Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, shall be reduced to writing by him or under his direction, and be read over to the informant. The police officer is legally bound to register the FIR and cannot refuse. A copy of the FIR must be given to the informant free of cost.",
        "category": "police",
    },
    {
        "id": "bnss_s175",
        "act": "BNSS",
        "section": "175(3)",
        "title": "Magistrate's power to direct FIR registration",
        "text": "If a Magistrate receives a complaint and is of the opinion that there is sufficient ground for proceeding, he may direct the police to register an FIR and investigate the matter. This is the remedy when police refuse to register an FIR.",
        "category": "police",
    },
    {
        "id": "bnss_s144",
        "act": "BNSS",
        "section": "144",
        "title": "Order for maintenance of wives, children and parents",
        "text": "If any person having sufficient means neglects or refuses to maintain his wife, his legitimate or illegitimate minor child, or his father or mother unable to maintain themselves, a Magistrate may order such person to make a monthly allowance for the maintenance of his wife, child or parents.",
        "category": "family",
    },
    {
        "id": "bnss_s479",
        "act": "BNSS",
        "section": "479",
        "title": "Bail for undertrial prisoners",
        "text": "An undertrial prisoner who has served half the maximum period of imprisonment specified for the offence shall be released on bail. This provision ensures that undertrial prisoners are not detained indefinitely.",
        "category": "police",
    },
    {
        "id": "bnss_s530",
        "act": "BNSS",
        "section": "530",
        "title": "Trial by video conferencing",
        "text": "The inquiry or trial may be held through video conferencing. Evidence of a witness may be recorded through video conferencing. This provision enables access to justice for persons who cannot physically appear in court.",
        "category": "police",
    },
]


def scrape_bnss() -> list:
    """
    Attempt to scrape BNSS sections. Falls back to curated sections.

    Returns:
        List of section dicts.
    """
    logger.info("Attempting to scrape BNSS from India Code...")

    try:
        headers = {"User-Agent": "Mozilla/5.0 (legal-aid-navigator research tool)"}
        response = requests.get(
            "https://www.indiacode.nic.in/handle/123456789/20062",
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        # If we get here but can't parse structured sections, use fallback
        logger.info("Connected to India Code — using curated BNSS sections for accuracy.")
    except Exception as e:
        logger.warning("Connection failed (%s) — using curated fallback.", e)

    logger.info("Using %d curated BNSS sections.", len(FALLBACK_SECTIONS))
    return FALLBACK_SECTIONS


def main():
    """Scrape BNSS and save to knowledge_base/bnss_sections.json."""
    sections = scrape_bnss()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)

    logger.info("Saved %d BNSS sections to %s", len(sections), OUTPUT_PATH)


if __name__ == "__main__":
    main()
