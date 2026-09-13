import os
from pathlib import Path

from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.storage.docstore import SimpleDocumentStore
from db import vector_store

import asyncio

embedding_model = 'nomic-embed-text';
def extract_metadata(filename: str):
    path = Path(filename)
    return {
        "file_name": path.name,
        "file_type": path.suffix.lower().replace(".", ""),  # e.g., 'pdf', 'txt', 'md'
    }
PIPELINE_STORAGE = "./pipeline_storage"

async def data_pipeline(context_data):
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_overlap=25, chunk_size=250),
            OllamaEmbedding(
                model_name="nomic-embed-text", 
                base_url="http://localhost:11434"
            )
        ],
        docstore=SimpleDocumentStore(),
        vector_store=vector_store
    )

    if os.path.exists(PIPELINE_STORAGE):
        pipeline.load(PIPELINE_STORAGE)
        print("-- Loaded existing docstore state! \n")

    nodes = await pipeline.arun(documents=context_data)
    if len(nodes) == 0:
        print ("-- Nothing to update. Your embeddings are up-to-date")
    else:
        print(f"Successfully processed and stored {len(nodes)} nodes in ChromaDB!")
        pipeline.persist(PIPELINE_STORAGE)


async def main():
    try:
        print("\n -- Initializing data read process... \n")
        documents = SimpleDirectoryReader("data", file_metadata=extract_metadata, filename_as_id=True).load_data()

        print("-- Data read process done... \n")
        print("-- Initialise Data embedding...")

        await data_pipeline(documents)
    except Exception as e:
        print(f"Failed to run ingestion pipeline. Error {e}")

if __name__== '__main__':
    print("Running ingestion pipeline...")
    asyncio.run(main())
    print("done!")
