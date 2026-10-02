""" This module explain the basic usage of inoking a model with cusotom tools
    In Langchain, if you are using chat_model APIs then you need to manage the
    conversational loop between model and tool, we need to invoke the tool and pass
    the result back to model as AIMessage so LLM can parse that and generate the result.

    NOTE: This conversational loop managed by agent automatically when we use 
    create_agent API, but with chat_models, this needs to be managed manually.
"""

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.messages import SystemMessage, HumanMessage, AIMessage


@tool("get_weather", description="use this tool to get the weather for any location")
def get_weather(location: str) -> str:
    return f"Weather at {location} is sunny!"


tools = [get_weather]
tools_by_name = {tool.name: tool for tool in tools}

# here using local ollama model, but you can use any provider,
# Make sure to load the API key for any cloud llm provider
model = init_chat_model('ollama:gemma4:12b-mlx')

model_with_tools = model.bind_tools(tools)
messages = [
    SystemMessage("You are a helpful assistant."),
    HumanMessage("How's the weather at SF and NYC?")
]

# invoke llm with Messages (with tools)
ai_message = model_with_tools.invoke(messages)

# update conversational history, so LLM remembers that it invoked a tool
messages.append(ai_message)

# invoke tool manually and pass the result back to llm
for tool_call in ai_message.tool_calls:
    tool = tools_by_name[tool_call.get('name', None)]
    tool_result = tool.invoke(tool_call)
    messages.append(tool_result)

response = model_with_tools.invoke(messages)

print(response.content) # The weather in both San Francisco and New York City is sunny!
print(f"input tokens: {response.usage_metadata.get('input_tokens')}")
print(f"output tokens: {response.usage_metadata.get('output_tokens')}")


