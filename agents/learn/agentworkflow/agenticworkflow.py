import asyncio
import os

from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from llama_index.llms.openrouter import OpenRouter

from dotenv import load_dotenv, find_dotenv

envpath = find_dotenv()
load_dotenv(envpath)
OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")


def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


def multiply(a: int, b: int) -> int:
    """multuply two numbers"""
    return a * b


async def main():
    llm = OpenRouter(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPEN_ROUTER_KEY,
    )
    add_agent = ReActAgent(
        name="add_agent",
        description="A helpful assitant that can use the tool to add to numbers",
        tools=[add],
        llm=llm,
    )

    multiply_agent = ReActAgent(
        name="multiply_agent",
        description="A helpful assitant that can use the tool to multiply two numbers",
        tools=[multiply],
        llm=llm,
    )
    print("Running the agent...")
    workflow = AgentWorkflow(
        agents=[add_agent, multiply_agent],
        root_agent="multiply_agent",
    )
    res = await workflow.run(user_msg="Can you add 4 and 3?")
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
