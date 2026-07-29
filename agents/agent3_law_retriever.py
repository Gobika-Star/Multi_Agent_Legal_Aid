import chromadb
from chromadb.utils import embedding_functions
import json
import os

# Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAWS_PATH = os.path.join(BASE_DIR, "knowledge_base", "laws.json")
CHROMA_DIR = os.path.join(BASE_DIR, "knowledge_base", "chroma_db")

# Local embedding model — no API cost, runs on CPU
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=CHROMA_DIR)


def build_knowledge_base():
    """
    One-time setup: loads laws.json and embeds it into ChromaDB.
    Safe to re-run — it recreates the collection each time.
    """
    try:
        client.delete_collection("laws")
    except Exception:
        pass

    collection = client.create_collection(
        name="laws",
        embedding_function=embedding_fn
    )

    with open(LAWS_PATH, "r", encoding="utf-8") as f:
        laws = json.load(f)

    collection.add(
        ids=[law["id"] for law in laws],
        documents=[law["text"] for law in laws],
        metadatas=[{"category": law["category"], "title": law["title"]} for law in laws]
    )

    print(f"Knowledge base built with {len(laws)} law entries.")
    return collection


def get_collection():
    """Fetch existing collection, building it if it doesn't exist yet."""
    try:
        return client.get_collection(name="laws", embedding_function=embedding_fn)
    except Exception:
        return build_knowledge_base()


def retrieve_laws(query: str, category: str, top_k: int = 3) -> list:
    """
    Retrieves the most relevant law excerpts, filtered by category first.
    """
    collection = get_collection()

    where_filter = {"category": category} if category != "other" else None

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter
    )

    laws = []
    if results["documents"] and results["documents"][0]:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            laws.append({
                "title": meta["title"],
                "text": doc,
                "category": meta["category"]
            })
    return laws


if __name__ == "__main__":
    build_knowledge_base()

    test_cases = [
        ("My landlord is not returning my deposit, it has been 3 months.", "land"),
        ("Someone hacked my Instagram and is asking for money.", "cyber"),
        ("My husband is not paying maintenance after our separation.", "family")
    ]

    for query, category in test_cases:
        print(f"\nQuery: {query} [{category}]")
        results = retrieve_laws(query, category)
        for r in results:
            print(f"  - {r['title']}: {r['text'][:80]}...")