from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_stream_writer
from exa_py import Exa

from dotenv import load_dotenv
import os

load_dotenv()

exa = Exa(os.getenv("EXA_API_KEY"))
llm = init_chat_model(
    model="gemma4:12b-mlx",
    model_provider="ollama",
    temperature=0.7,
    timeout=60,
    base_url="http://localhost:11434",
    num_predict=16334,
)


@tool("search", description="Search internet for any query")
def search_tool(query: str):
    writer = get_stream_writer()
    writer({"status": f"using search tool to query ~{query}"})
    result = exa.search(
        query,
        num_results=5,
        type="auto",
    )
    return result


agent = create_agent(
    model=llm,
    tools=[search_tool],
    checkpointer=InMemorySaver(),
    system_prompt="You are an expert chef and helping assistant, who specialises in making all kinds of dishes based on available ingredients.",
)


# res = llm.stream([
#     SystemMessage("You are an helpful assistant"),
#     HumanMessage("What tool access you have? do you have ability to search internet at the moment? If No, then simply say 'No', else tell me what's the current time in India?")
# ])

config: RunnableConfig = { "configurable": { "thread_id": str(uuid7())}}

result = agent.stream(
    {"messages": [HumanMessage(content="I have 3 tomatoes, some broccoli, mashed potatoes and all spices, tell me 3 top dishes I can make using these?")]},
    version="v2",
    config=config,
    stream_mode=["messages", 'custom', 'updates']
)

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)
    # N.B. all content is available through token.content_blocks

def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        d = message.tool_calls[-1]
        for key, _ in d.items():
            if d[key] == 'search':
                print(f"searching for {d['args']['query']}")
    if isinstance(message, ToolMessage):
        pass
        # uncommet this to print the tool response
        #print(f"Tool response: {message.content_blocks}")

for chunk in result:
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "custom":
        if 'status' in chunk['data']:
            print(chunk['data']['status'])
    elif chunk["type"] == "updates":
        for source, update in chunk["data"].items():
            if source in ("model", "tools"):  # `source` captures node name
                _render_completed_message(update["messages"][-1])
