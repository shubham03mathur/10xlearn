from llama_index.core.base.response.schema import StreamingResponse
from query_engine_synthesizer import query_engine

print("Thinking...\n")
res = query_engine.query("What are the common features of FastAPI? What makes it the best choice in 2026?")

if isinstance(res, StreamingResponse):
    res.print_response_stream()
else:
    print(res)

print("\n\n--- Source Nodes Used ---")
for node in res.source_nodes:
    print(f"Score: {node.score} | File: {node.metadata.get('file_name', 'Unknown')}")