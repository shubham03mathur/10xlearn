from llama_index.core.evaluation import FaithfulnessEvaluator
from .rag import get_query_engine, llm

evaluator = FaithfulnessEvaluator(llm=llm)

response = get_query_engine().query("Does Florida has rent control laws?")

evaluation = evaluator.evaluate_response(response=response)

print(evaluation.passing)