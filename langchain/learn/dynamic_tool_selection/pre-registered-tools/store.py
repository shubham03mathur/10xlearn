"""
This module demonstrate how we can use runtime context to dynamically load tool based on
permissions, feature flag or authentication state.

This approach works when:
 - All possible tools are known at the compile/startup time.
 - You want to filter based on permissions, feature flags, or conversation state.
 - Tools are static but their availability is dynamic.
"""

from typing import Callable
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelResponse, ModelRequest
from langchain.chat_models import init_chat_model
from langgraph.store.memory import InMemoryStore

""" reusing the tools """
from state import advanced_search, private_search, public_search

@dataclass
class User:
    user_id: str

@wrap_model_call
def store_based_tools(
    request: ModelRequest[User],
    handler: Callable[[ModelRequest[User]], ModelResponse]
) -> ModelResponse:

    user_id = request.runtime.context.user_id
    if user_id:
        store = request.runtime.store
        feature_flags = store.get(('features', ), user_id)
    if not user_id:
        tools = [t for t in request.tools if t.name.startswith("public_")]
        request.override(tools=tools)
    else:
        enabled_features = feature_flags.value.get("enabled_tools", [])
        """ Only enable features for this user """
        tools = [t for t in request.tools if t.name in enabled_features]
        request.override(tools=tools)

    return handler(request)

llm = init_chat_model('ollama:gemma4:12b-mlx')

agent = create_agent(
    model=llm,
    tools=[public_search, private_search, advanced_search],
    middleware=[store_based_tools],
    context_schema=User,
    store=InMemoryStore()
)
