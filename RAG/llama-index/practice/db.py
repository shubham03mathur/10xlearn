import chromadb
from pathlib import Path
from llama_index.vector_stores.chroma import ChromaVectorStore

PATH = Path(__file__).resolve().parent.parent / 'xarvis_db'

db = chromadb.PersistentClient(path=str(PATH))
collection = db.get_or_create_collection('xarvis')
vector_store = ChromaVectorStore(chroma_collection=collection)