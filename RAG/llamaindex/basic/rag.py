from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from .indexing import get_index

LLM_MODEL_NAME = "Qwen/Qwen2.5-Coder-32B-Instruct"
DEFAULT_QUERY = (
    "Does Florida has rent control laws? Provide the citations as well as a link"
)


def get_query_engine():
    llm = HuggingFaceInferenceAPI(model_name=LLM_MODEL_NAME)
    return get_index().as_query_engine(
        llm=llm,
        response_mode="tree_summarize",
    )


def run(query: str = DEFAULT_QUERY) -> None:
    query_engine = get_query_engine()
    response = query_engine.query(query)
    print(response)


if __name__ == "__main__":
    run()
