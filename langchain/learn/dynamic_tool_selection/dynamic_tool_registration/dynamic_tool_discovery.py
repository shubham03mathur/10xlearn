"""
So far in previous modules we have seen how we can control the tool access based on
state, context or store, however in all cases the tools were pre-registered and were
available at runtime but in practical scenarios and real-world meaningful projects,
You would need to access/load the tool on-demand, dynamically either from another server
or via MCP.

In this module we will learn how we can load the tool from other resources on-demand.
Fundamentally, this appraoch requires, two major hooks:
 - *wrap_model_response*
 - *wrap_tool_call*

"""
from typing import Any, Callable
from langchain.agents import create_agent
from langchain.agents.middleware.types import ExtendedModelResponse
from langchain.tools import tool
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain.chat_models import init_chat_model
from dataclasses import dataclass

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command

@tool
def calculate_tax(total_bill: float, tax: float = 10.0):
    total_tax = total_bill * (tax / 100)
    return f" tax amount: {total_tax}, total amount: {total_bill + total_tax}"

class DynamicToolDiscovery(AgentMiddleware):
    """ Dynamic tool discovery middleware, which registers and handle dynamic tools """

    def wrap_model_call(self, request: ModelRequest[None], handler: Callable[[ModelRequest[None]], ModelResponse[Any]]) -> ModelResponse[Any] | AIMessage | ExtendedModelResponse[Any]:
        super().wrap_model_call(request, handler)
        """
            Add dynamic tool to the request. This can be loaded
            from any resource such as another instance, database or MCP server.
        """
        updated = request.override(tools=[*request.tools, calculate_tax])
        return handler(updated)

    def wrap_tool_call(self, request: ToolCallRequest, handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]]) -> ToolMessage | Command[Any]:
        super().wrap_tool_call(request, handler)

        """ intercept the tool call and invoke the custom tool"""
        if request.tool_call.get('name') == 'calculate_tax':
            return handler(request.override(tool=calculate_tax))

        return handler(request)

agent = create_agent(
    model=init_chat_model('ollama:gemma4:12b-mlx'),
    tools=[], # add any static/pre-defined tool
    middleware=[DynamicToolDiscovery()]
)