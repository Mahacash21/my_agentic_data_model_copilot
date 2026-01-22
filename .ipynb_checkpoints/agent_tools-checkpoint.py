from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = "vectorstore/architecture"

# --- Embedding model (updated, non-deprecated) ---
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# --- Load vector store ---
db = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings
)


def _sanitize_rag_text(text: str) -> str:
    """
    Remove agent-like or system instructions from RAG content
    to prevent planner contamination.
    """
    forbidden_phrases = [
        "You are",
        "Available actions",
        "Rules:",
        "SYSTEM",
        "Respond with",
        "Begin only after",
        "Tasked with",
        "You must"
    ]

    cleaned = text
    for phrase in forbidden_phrases:
        cleaned = cleaned.replace(phrase, "")

    return cleaned.strip()


def architecture_rag_tool(question: str, k: int = 5):
    """
    Architecture RAG lookup tool

    Returns:
    {
        "context": str,   # clean concatenated architecture knowledge
        "sources": [str]  # unique source references
    }
    """
    results = db.similarity_search(question, k=k)

    if not results:
        return {
            "context": "",
            "sources": []
        }

    context_chunks = []
    sources = set()

    for r in results:
        category = r.metadata.get("category", "unknown")
        source = r.metadata.get("source", "unknown")

        chunk = f"[{category}] {r.page_content}"
        chunk = _sanitize_rag_text(chunk)

        context_chunks.append(chunk)
        sources.add(f"{source} ({category})")

    context = "\n\n".join(context_chunks)

    return {
        "context": context,
        "sources": sorted(sources)
    }
