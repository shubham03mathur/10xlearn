"""
Module for demonstrating a basic AgentWorkflow setup.

This module illustrates how to coordinate multiple agents using the 
AgentWorkflow framework to handle simple, independent tasks.
"""
import asyncio
import os
 
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from llama_index.llms.openrouter import OpenRouter
 
from dotenv import load_dotenv, find_dotenv
 
envpath = find_dotenv()
load_dotenv(envpath)
OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")



def add(a: int, b: int) -> int:
    """
    Adds two integers.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        The sum of a and b.
    """
    return a + b


def multiply(a: int, b: int) -> int:
    """
    Multiplies two integers.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        The product of a and b.
    """
    return a * b


async def main():
    """
    Entry point for the basic agent workflow.
    Initializes agents, defines the workflow, and executes a sample addition query.
    """
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
