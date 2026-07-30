"""
scraper/scrape_bns.py
Scraper for Bharatiya Nyaya Sanhita (BNS), 2023.

Fetches section data from India Code (indiacode.nic.in) and saves
structured JSON to knowledge_base/bns_sections.json.

Run: python scraper/scrape_bns.py
"""

import json
import os
import time
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "knowledge_base", "bns_sections.json")

# India Code BNS act page
BNS_URL = "https://www.indiacode.nic.in/bitstream/123456789/20062/1/a2023-45.pdf"

# Fallback: curated key sections for offline use
FALLBACK_SECTIONS = [
    {
        "id": "bns_s61",
        "act": "BNS",
        "section": "61",
        "title": "Attempt to commit offences",
        "text": "Whoever attempts to commit an offence punishable by this Sanhita with imprisonment for life or imprisonment, or to cause such an offence to be committed, and in such attempt does any act towards the commission of the offence, shall be punished.",
        "category": "police",
    },
    {
        "id": "bns_s74",
        "act": "BNS",
        "section": "74",
        "title": "Assault or criminal force to woman with intent to outrage her modesty",
        "text": "Whoever assaults or uses criminal force to any woman, intending to outrage or knowing it to be likely that he will thereby outrage her modesty, shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both.",
        "category": "police",
    },
    {
        "id": "bns_s85",
        "act": "BNS",
        "section": "85",
        "title": "Cruelty by husband or his relatives",
        "text": "Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be punished with imprisonment for a term which may extend to three years and shall also be liable to fine.",
        "category": "family",
    },
    {
        "id": "bns_s115",
        "act": "BNS",
        "section": "115",
        "title": "Voluntarily causing grievous hurt",
        "text": "Whoever voluntarily causes grievous hurt shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
        "category": "police",
    },
    {
        "id": "bns_s318",
        "act": "BNS",
        "section": "318",
        "title": "Cheating",
        "text": "Whoever cheats shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both. Whoever cheats with the knowledge that he is likely thereby to cause wrongful loss to a person whose interest he is bound to protect shall be punished with imprisonment of either description for a term which may extend to five years.",
        "category": "cyber",
    },
    {
        "id": "bns_s329",
        "act": "BNS",
        "section": "329",
        "title": "Mischief",
        "text": "Whoever commits mischief shall be punished with imprisonment of either description for a term which may extend to six months, or with fine, or with both. Mischief causing damage to property worth fifty rupees or more is punishable with imprisonment up to two years.",
        "category": "land",
    },
    {
        "id": "bns_s351",
        "act": "BNS",
        "section": "351",
        "title": "Criminal intimidation",
        "text": "Whoever threatens another with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested, with intent to cause alarm to that person, or to cause that person to do any act which he is not legally bound to do, commits criminal intimidation. Punishment: imprisonment up to two years, or fine, or both.",
        "category": "cyber",
    },
]


def scrape_bns() -> list:
    """
    Attempt to scrape BNS sections from India Code.
    Falls back to curated offline sections if scraping fails.

    Returns:
        List of section dicts with id, act, section, title, text, category.
    """
    logger.info("Attempting to scrape BNS from India Code...")

    try:
        headers = {"User-Agent": "Mozilla/5.0 (legal-aid-navigator research tool)"}
        response = requests.get(
            "https://www.indiacode.nic.in/handle/123456789/20062",
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        # Try to extract section data from the page
        sections = []
        section_divs = soup.find_all("div", class_="section") or soup.find_all("p")

        if len(section_divs) > 5:
            for i, div in enumerate(section_divs[:50]):
                text = div.get_text(strip=True)
                if len(text) > 50:
                    sections.append({
                        "id": f"bns_scraped_{i}",
                        "act": "BNS",
                        "section": str(i),
                        "title": text[:60],
                        "text": text[:500],
                        "category": "police",
                    })

        if sections:
            logger.info("Scraped %d sections from India Code.", len(sections))
            return sections

    except Exception as e:
        logger.warning("Scraping failed (%s) — using curated fallback sections.", e)

    logger.info("Using %d curated BNS sections.", len(FALLBACK_SECTIONS))
    return FALLBACK_SECTIONS


def main():
    """Scrape BNS and save to knowledge_base/bns_sections.json."""
    sections = scrape_bns()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)

    logger.info("Saved %d BNS sections to %s", len(sections), OUTPUT_PATH)


if __name__ == "__main__":
    main()
