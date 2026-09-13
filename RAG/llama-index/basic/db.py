from pathlib import Path

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

DB_PATH = Path(__file__).resolve().parent / "xarvis_db"

db = chromadb.PersistentClient(path=str(DB_PATH))
chroma_collection = db.get_or_create_collection("Xarvis")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
