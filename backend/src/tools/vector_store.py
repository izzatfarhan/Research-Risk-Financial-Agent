# backend/src/tools/vector_store.py
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Define local data and DB directories
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = BACKEND_DIR / "storage"
DB_DIR = STORAGE_DIR / "chroma_db"
DOCS_DIR = STORAGE_DIR / "docs"

# Ensure directories exist
DB_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

print("⏳ [Engine] Mounting local Hugging Face Embedding Model (BGE)...")
# Load embedding model locally from Hugging Face
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'} # Change to 'cuda' if you have an Nvidia GPU
)
print("🔥 [Engine] Embedding engine active.")

def ingest_pdf_to_vector_store(pdf_filename: str):
    """Parses a local PDF, splits text into chunks, and commits to Chroma DB."""
    pdf_path = DOCS_DIR / pdf_filename
    if not pdf_path.exists():
        print(f"⚠️ Ingestion skipped: {pdf_filename} not found in {DOCS_DIR}")
        return None
        
    print(f"📄 [RAG] Loading document: {pdf_filename}...")
    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()
    
    # Financial data requires tight chunk overlays to preserve structural numeric data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    
    print(f"🧬 [RAG] Generating embeddings for {len(docs)} text segments...")
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=str(DB_DIR)
    )
    print("✅ [RAG] Document vectors successfully committed to database storage.")
    return vector_store

def get_vector_store_retriever():
    """Returns a retriever handler to search ingested documents."""
    return Chroma(
        persist_directory=str(DB_DIR), 
        embedding_function=embedding_model
    ).as_retriever(search_kwargs={"k": 3})