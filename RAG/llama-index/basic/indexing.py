from functools import lru_cache

from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from .db import vector_store

EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"


@lru_cache(maxsize=1)
def get_index() -> VectorStoreIndex:
    embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
    return VectorStoreIndex.from_vector_store(
        embed_model=embed_model,
        vector_store=vector_store,
    )
