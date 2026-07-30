"""
build_kb.py
Master script to build the complete knowledge base.

1. Runs all scrapers to generate JSON files
2. Merges all JSON files into ChromaDB

Run once before starting the application:
  python build_kb.py
"""

import json
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")

# All JSON knowledge base files to merge into ChromaDB
KB_FILES = [
    os.path.join(KB_DIR, "laws.json"),
    os.path.join(KB_DIR, "bns_sections.json"),
    os.path.join(KB_DIR, "bnss_sections.json"),
    os.path.join(KB_DIR, "bsa_sections.json"),
]


def run_scrapers():
    """Run all scrapers to generate JSON files."""
    from scraper.scrape_bns import main as scrape_bns
    from scraper.scrape_bnss import main as scrape_bnss
    from scraper.scrape_bsa import main as scrape_bsa

    logger.info("Running scrapers...")
    scrape_bns()
    scrape_bnss()
    scrape_bsa()
    logger.info("All scrapers completed.")


def merge_and_build():
    """Merge all JSON files and rebuild ChromaDB collection."""
    from agents.agent3_law_retriever import build_knowledge_base, _chroma_client
    import chromadb
    from chromadb.utils import embedding_functions

    all_laws = []
    seen_ids = set()

    for path in KB_FILES:
        if not os.path.exists(path):
            logger.warning("File not found, skipping: %s", path)
            continue

        with open(path, "r", encoding="utf-8") as f:
            laws = json.load(f)

        for law in laws:
            if law["id"] not in seen_ids:
                # Ensure all required fields exist
                law.setdefault("category", "other")
                law.setdefault("title", law.get("act", "Unknown") + " Section " + law.get("section", "?"))
                all_laws.append(law)
                seen_ids.add(law["id"])

    logger.info("Total unique law entries to index: %d", len(all_laws))

    # Write merged file
    merged_path = os.path.join(KB_DIR, "laws_merged.json")
    with open(merged_path, "w", encoding="utf-8") as f:
        json.dump(all_laws, f, ensure_ascii=False, indent=2)

    # Rebuild ChromaDB
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    chroma_dir = os.path.join(KB_DIR, "chroma_db")
    client = chromadb.Client(
        chromadb.config.Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=chroma_dir,
            anonymized_telemetry=False,
        )
    )

    try:
        client.delete_collection("laws")
    except Exception:
        pass

    collection = client.create_collection(name="laws", embedding_function=embedding_fn)
    collection.add(
        ids=[law["id"] for law in all_laws],
        documents=[law["text"] for law in all_laws],
        metadatas=[{"category": law["category"], "title": law["title"]} for law in all_laws],
    )

    logger.info("ChromaDB rebuilt with %d entries.", len(all_laws))
    return len(all_laws)


if __name__ == "__main__":
    run_scrapers()
    count = merge_and_build()
    print(f"\n✅ Knowledge base ready — {count} law entries indexed in ChromaDB.")
