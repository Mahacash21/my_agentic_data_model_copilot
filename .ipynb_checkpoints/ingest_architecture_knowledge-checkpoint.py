import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


BASE_PATH = "architecture_knowledge"
PERSIST_DIR = "vectorstore/architecture"

embeddings = OllamaEmbeddings(model="nomic-embed-text")

documents = []

for root, _, files in os.walk(BASE_PATH):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)

            loader = TextLoader(path, encoding="utf-8")
            docs = loader.load()

            for doc in docs:
                doc.metadata = {
                    "source": file,
                    "category": os.path.basename(root),
                    "path": path
                }
                documents.append(doc)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

db = Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory=PERSIST_DIR
)

db.persist()

print(f"Ingested {len(chunks)} architecture knowledge chunks.")
