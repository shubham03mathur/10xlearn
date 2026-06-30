from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from .indexing import index

llm = HuggingFaceInferenceAPI(model_name="Qwen/Qwen2.5-Coder-32B-Instruct")
query_engine = index.as_query_engine(
    llm=llm,
    response_mode="tree_summarize"
)

response = query_engine.query("Does Florida has rent control laws? Provide the citations as well as a link")
print(response)
