"""
This module demonstrate how we can use runtime context state to dynamically load tool based on
permissions, feature flag or authentication state.

This approach works when:
 - All possible tools are known at the compile/startup time.
 - You want to filter based on permissions, feature flags, or conversation state.
 - Tools are static but their availability is dynamic.

"""
from typing import Callable
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

@tool('advanced_search')
def advanced_search():
   """ use this tool to perform deep research about any topic """
   pass

@tool('public_search')
def public_search():
    """ use this tool for any general purpose search """
    pass

@tool('private_search')
def private_search():
    """ use this tool to search about any topic without user's data profile """
    pass

@wrap_model_call
def state_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """ filter based on conversational state """
    state: AgentState = request.state
    authenticated = state.get('is_authenticated', False)
    message_count = len(state["messages"])

    is_premium_user = state.get('is_premium', False)
    if not authenticated:
        # if user is not logged in then they may have access to only non sensitive tools
        tools = [t for t in request.tools if t.name.startswith("public_")]
        request = request.override(tools=tools)
    else:
        # premium user gets full access and users without subscription don't get
        # access to advanced_search if message count is less than 5
        if not is_premium_user and message_count < 5:
            tools = [t for t in request.tools if t.name != 'advanced_search']

    return handler(request)

# using local ollama model, you can switch to any provider
llm = init_chat_model('ollama:gemma4:12b-mlx')
agent = create_agent(
    model=llm,
    tools=[public_search, private_search, advanced_search],
    middleware=[state_based_tools]
)

res = agent.invoke({
    "messages" : [
        SystemMessage("you are an helpful assistance who have access to provided user defined tools only."),
        HumanMessage("What custom tools you have access to? Describe them")]
})

"""
(since user isn't logged in, it should have access to only public search):

I have access to the following custom tool:

**public_search**
*   **Description:** This tool allows me to perform general-purpose searches to find information,
    news, and data from the internet. I can use it whenever you ask a question that requires
    up-to-date information or a broad search of available web content.
"""
for message in res["messages"]:
    if isinstance(message, AIMessage):
        print(message.text)