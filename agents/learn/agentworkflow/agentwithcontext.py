"""
Module for demonstrating AgentWorkflows with persistent context.

This module illustrates how to use the `Context` object to maintain state 
(e.g., counting function calls) across multiple agent turns.
"""
"""
Module for demonstrating AgentWorkflows with persistent context.

This module illustrates how to use the `Context` object to maintain state 
(e.g., counting function calls) across multiple agent turns.
"""
import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from llama_index.core.workflow import Context
from llama_index.llms.openrouter import OpenRouter

envpath = find_dotenv()
load_dotenv(envpath)


OPEN_AI_KEY = os.getenv("OPEN_ROUTER_KEY")


async def addition(ctx: Context, a: int, b: int) -> int:
    """
    Adds two integers and updates the shared state count.

    Args:
        ctx: The execution context containing the shared state.
        a: The first integer.
        b: The second integer.

    Returns:
        The sum of a and b.
    """
    curr_state = await ctx.store.get("state", default={"num_fn_calls": 0})
    curr_state["num_fn_calls"] += 1
    await ctx.store.set('state', curr_state)
    return a + b


async def multiply(ctx: Context, a: int, b: int) -> int:
    """
    Multiplies two integers and updates the shared state count.

    Args:
        ctx: The execution context containing the shared state.
        a: The first integer.
        b: The second integer.

    Returns:
        The product of a and b.
    """
    curr_state = await ctx.store.get("state", default={"num_fn_calls": 0})
    curr_state["num_fn_calls"] += 1
    await ctx.store.set('state', curr_state)
    return a * b


async def main():
    """
    Entry point for the multiplication example.
    Initializes the agents, defines the workflow, and executes a sample query.
    """
    llm = OpenRouter(api_base="https://openrouter.ai/api/v1", api_key=OPEN_AI_KEY)


    multiply_agent = ReActAgent(
        name="multiply_agent",
        description="You are a helpful assitant and can use tool to perform multiplication of two numbers.",
        tools=[multiply],
        llm=llm,
        can_handoff_to=["addition_agent"]
    )

    addition_agent = ReActAgent(
        name="addition_agent",
        description="You are a helpful assistant and can use tool to perform addition of two numbers.",
        tools=[addition],
        llm=llm,
        can_handoff_to=["multiply_agent"]
    )

    

    workflow = AgentWorkflow(
        agents=[addition_agent, multiply_agent],
        root_agent="multiply_agent",
        initial_state={"num_fn_calls": 0},
        state_prompt="Current state: {state}. User message: {msg}",
        early_stopping_method='generate',
    )

    ctx = Context(workflow)

    res = await workflow.run(user_msg="Can you multiply 100 and 56?", ctx=ctx)
    print(res)

    st = await ctx.store.get("state")
    print(f"Total no of function call(s): {st.get('num_fn_calls', 'Could not retrieve value')}")


if __name__ == "__main__":
    print("Executing workflow...")
    asyncio.run(main())
    print("done!")
