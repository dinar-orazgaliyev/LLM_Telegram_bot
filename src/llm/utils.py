from pypdf import PdfReader
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import os

pdf_files = {
    "A1": ["A1-1.pdf", "Preview-9-German-Grammar-Exercises-Level-A1-A2.pdf"],
    "A2": [
        "A2-1.pdf",
        "A2-2.pdf",
        "Preview-9-German-Grammar-Exercises-Level-A1-A2.pdf",
    ],
    "B1": ["B1.pdf", "B1_Uebungssatz_Erwachsene.pdf"],
    # "General" could store 'Basic german.pdf' if it covers multiple levels
    "General": ["Basic german.pdf"],
}


def extract_text_from_pdf(path: Path) -> str:
    """Extract all text from a PDF file."""
    text = ""
    reader = PdfReader(path)
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


def load_pdfs(pdf_files: dict, rag_dir: Path) -> dict:
    """Load and combine PDFs per level."""
    pdf_texts = {}
    for level, files in pdf_files.items():
        combined_text = ""
        for f in files:
            combined_text += extract_text_from_pdf(rag_dir / f) + "\n"
        pdf_texts[level] = combined_text
    return pdf_texts


# ---------- RAG Utils ----------
def split_into_chunks(pdf_texts: dict, chunk_size=500, overlap=50):
    """Split text into small chunks with metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )
    all_docs = []
    for level, text in pdf_texts.items():
        docs = splitter.create_documents([text], metadatas=[{"level": level}])
        all_docs.extend(docs)
    return all_docs


def build_vector_db(all_docs, persist_dir: Path):
    """Build and persist a Chroma vector database."""
    embeddings = OllamaEmbeddings(model="phi3")
    db = Chroma.from_documents(all_docs, embeddings, persist_directory=str(persist_dir))
    return db


def load_vector_db(persist_dir: Path):
    """Load an existing Chroma database."""
    embeddings = OllamaEmbeddings(model="phi3")
    return Chroma(persist_directory=str(persist_dir), embedding_function=embeddings)


def query_vector_db(db, query: str, k=3, level: str = None):
    """Query the vector DB with optional level filter."""
    filter_dict = {"level": level} if level else None
    return db.similarity_search(query, k=k, filter=filter_dict)


def init_vector_db(rag_dir: Path):
    """Build vector DB if not exists, otherwise load it."""
    db_path = rag_dir / "chroma_db"
    if db_path.exists() and any(db_path.iterdir()):
        print("Loading existing vector DB...")
        return load_vector_db(db_path)
    else:
        print("Building new vector DB...")
        pdf_texts = load_pdfs(pdf_files, rag_dir)
        docs = split_into_chunks(pdf_texts)
        return build_vector_db(docs, db_path)


if __name__ == "__main__":
    pdf_texts = {}
    root = Path(os.getcwd())
    rag_dir = root / "data_rag"
    # pdf_texts = load_pdfs(pdf_files, rag_dir)
    # docs = split_into_chunks(pdf_texts)
    # db = build_vector_db(docs, rag_dir / "chroma_db")
    db = init_vector_db(rag_dir=rag_dir)
    collection = db._collection  # the actual Chroma collection object

    # Get some info
    # print("Number of documents:", collection.count())
    # print("Collection metadata:", collection.get(include=["metadatas", "documents"], limit=5))

    # For testing purposes
    results = db.similarity_search("Wie heißt du?", k=3, filter={"level": "A1"})
    for r in results:
        print(r.page_content)
