import os
import asyncio
from pathlib import Path

from datasets import load_dataset
from llama_index.core import Document
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from .db import vector_store

from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv(".env")
PROJECT_ROOT = Path(dotenv_path).parent

load_dotenv(PROJECT_ROOT)
HF_TOKEN = os.getenv("HF_TOKEN")

def prepare_context(dataset):
    print("Preparing Data...")
    refined_data = []
    for row in dataset:
        state = row.get("state", "Unknown")
        category = row.get("category", "Unknown")
        state_abv = row.get("state_abbr", "Unknown")

        context_string = (
            f"State: {state} ({state_abv})\n"
            f"Category: {category}\n"
            f"Question/Scenario: {row['instruction']} {row['input']}\n"
            f"Law/Guideline: {row['output']}"
        )

        # Return the text chunk, and isolate fields for vector DB metadata fields
        refined_data.append(
            Document(
                text=context_string,
                metadata={
                    "meta_state": state_abv,
                    "meta_category": row["category"],
                    "meta_source": row["source"],
                },
            )
        )

    return refined_data


async def create_pipeline(context_data):
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_overlap=25, chunk_size=250),
            HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5"),
        ],
        vector_store=vector_store,
    )

    nodes = await pipeline.arun(documents=context_data)
    print(f"Successfully processed and stored {len(nodes)} nodes in ChromaDB!")


async def main():
    try:
        print("Retrieving dataset...")
        hf_dataset = load_dataset(
            "ryancdossey1/2026-landlord-vs-tenant-state-rankings-index",
            name="faq",
            split="train",
        )
        context_data = prepare_context(hf_dataset)
        print("Data preparation done!")

        # Prepare dataset for ingestion
        await create_pipeline(context_data)
    except Exception as e:
        print(f"Failed to run ingestion pipeline. Error {e}")


if __name__ == "__main__":
    print("Running ingestion pipeline...")
    asyncio.run(main())
    print("Done!")
