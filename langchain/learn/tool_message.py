"""
This module explores how model processes the tool call and corresponding result, which
can be passed directly to the model for conversation, This module's objective is to understand
how langchain passes AIMessage and ToolMessage to the llm for processing and generates result.

To underatand how to call custom tools with langchain, visit ./model_with_basic_tool.py module.
"""

from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, ToolMessage, HumanMessage
from langchain_core.utils.uuid import uuid7

model = init_chat_model('ollama:gemma4:12b-mlx')
call_id = str(uuid7()) #this can be any unique id but must match with call ID
ai_message = AIMessage(
    content=[],
    tool_calls=[{
        "name": "get_weather",
        "args": { "location": "New York"},
        "id": call_id
    }]
)

tool_result = ToolMessage(
    content="Sunny, 72F!",
    tool_call_id=call_id
)

messages = [
    HumanMessage("What's the weather in New York?"),
    ai_message,
    tool_result
]

res = model.invoke(messages)

print(res.text) # The weather in New York is currently Sunny, 72°F.