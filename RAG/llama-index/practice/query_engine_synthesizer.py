from functools import lru_cache
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import LLMRerank
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

from db import vector_store

embedding_engine = OllamaEmbedding(
    model_name='nomic-embed-text',
    base_url="http://localhost:11434"
)

llm = Ollama(
    model="gemma4:12b-mlx",
    base_url="http://localhost:11434",
    request_timeout=120.0
)

@lru_cache(maxsize=1)
def get_index() -> VectorStoreIndex:
    return VectorStoreIndex.from_vector_store(
        embed_model=embedding_engine,
        vector_store=vector_store
    )

reranker = LLMRerank(
    llm=llm, 
    top_n=4
)
retriever = VectorIndexRetriever(
    index=get_index(),
    similarity_top_k=10,
)

response_synthesizer = get_response_synthesizer(llm=llm, streaming=True, response_mode=ResponseMode.TREE_SUMMARIZE)

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[reranker],
)