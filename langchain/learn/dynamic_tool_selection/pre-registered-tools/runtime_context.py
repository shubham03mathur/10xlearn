from typing import Callable
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from dataclasses import dataclass
from langchain.tools import tool

@tool
def view_data():
    pass

@tool
def write_data():
    pass

@tool
def delete_data():
    pass

@dataclass
class User:
    user_role: str

@wrap_model_call
def get_runtime_context(
    request: ModelRequest[User],
    handler: Callable[[ModelRequest[User]], ModelResponse]
) -> ModelResponse:
    """ Filter tools based on runtime context """
    if request.runtime is None or request.runtime.context is None:
        user_role = 'viewer'
    else:
        user_role = request.runtime.context.user_role

    if user_role == 'admin':
        """ admin has full access """
        pass
    elif user_role == 'editor':
        """ editor should not have access to delete data """
        tools = [t for t in request.tools if not t.name.startswith('delete_')]
        request.override(tools=tools)
    else:
        """ else viewer should only get read access """
        tools = [t for t in request.tools if t.name.startswith('view_')]
        request.override(tools=tools)

    return handler(request)

llm = init_chat_model('ollama:gemma4:12b-mlx')

create_agent(
    model=llm,
    tools=[view_data, write_data, delete_data],
    middleware=[get_runtime_context],
    context_schema=User
)
