from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

PERSIST_DIR = "vectorstore/architecture"

# Embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Load vector store
db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

def architecture_rag_tool(question: str, k: int = 5):
    """
    Returns:
    {
        "context": str,  # concatenated content chunks
        "sources": [str] # list of source filenames + categories
    }
    """
    results = db.similarity_search(question, k=k)

    context = "\n\n".join(
        f"[{r.metadata['category']}] {r.page_content}"
        for r in results
    )

    sources = list({
        f"{r.metadata['source']} ({r.metadata['category']})"
        for r in results
    })

    return {
        "context": context,
        "sources": sources
    }
