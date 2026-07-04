"""
The modules `agentwithcontext.py` and `agenticworkflow.py` both work well as long as the task is
simple and requires only a single function call. However, as soon as a user asks for something
that requires a multi-step process in conjunction—such as "Add two numbers a and b and then
multiply the result of it by 100" — these agents fail to answer correctly most of the time.

The reason behind this isn't that they are unable to hand off control to the other agent.
Instead, because the multiply_agent is set as the root_agent, it receives the user's prompt first.
Since the prompt contains numbers that fit its own tool signature, it eagerly decides to execute
its own tool first rather than forwarding it to the addition_agent.

This greedy routing completely disrupts the required order of operations, which ultimately
causes a precision error.

Here I will explain how we can use the `supervisor agent` to analyse and decide which tool/agent
should handle the query or intermidiate result and when.

"""

import os
import asyncio
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from llama_index.llms.openrouter import OpenRouter
from llama_index.core.workflow import Context

from dotenv import load_dotenv, find_dotenv

envpath = find_dotenv()
load_dotenv(envpath)
OEPN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")

async def addition(ctx: Context, a: int, b: int) -> int:
    """Add two numbers a and b"""
    async with ctx.store.edit_state() as store:
        store["state"]["fn_call_count"] += 1
    return a + b

async def multiply(ctx: Context, a: int, b: int) -> int:
    """Multiply two numbers a and b"""
    async with ctx.store.edit_state() as store:
        store["state"]["fn_call_count"] += 1
    return a * b

llm = OpenRouter(api_base="https://openrouter.ai/api/v1", api_key=OEPN_ROUTER_KEY)

async def main():

    addition_agent = ReActAgent(
        name="addition_agent",
        description=(
            "You can ONLY perform addition using your tool. "
            "If the task requires multiplication at any point, you MUST use the handoff tool to pass the current result to the multiply_agent. "
            "NEVER attempt to multiply numbers yourself without a tool."
        ),
        tools=[addition],
        llm=llm,
        can_handoff_to=["multiplication_agent", "supervisor_agent"],
    )

    multiplication_agent = ReActAgent(
        name="multiplication_agent",
        description=(
            "You can ONLY perform multiplication using your tool. "
            "If the task requires addition at any point, you MUST use the handoff tool to pass the current result to the addition_agent. "
            "NEVER attempt to add numbers yourself without a tool."
        ),
        tools=[multiply],
        llm=llm,
        can_handoff_to=["addition_agent", "supervisor_agent"],
    )

    review_agent = ReActAgent(
        name="review_agent",
        description=(
            "You are the review agent for math operations. "
            "You will receive the task solution from the supervisor agent in this format: "
            "{'query': msg, 'result': final_answer} "
            "Your job is to verify if the answer is correct using your tools. NEVER do the math yourself without a tool. "
            "If the answer is correct, return the result. If it is wrong, send it back to supervisor_agent to fix it."
        ),
        tools=[addition, multiply],
        llm=llm,
        can_handoff_to=["supervisor_agent"],
    )

    supervisor_agent = ReActAgent(
        name="supervisor_agent",
        description=(
            "You are a helpful assistant and supervisor. You need to understand the user's query "
            "and decide which agent should handle it first based on the mathematical order of operations (PEMDAS/BODMAS). "
            "Understand that '+' means addition and '*' means multiplication. Expressions inside parentheses '()' MUST be routed first. "
            "NEVER calculate the answer yourself. You MUST hand off the first operation to the correct specialized agent. "
            "Once the specialized agents complete all operations, you will receive the final result. "
            "Only then should you hand off the result to the review_agent in the following format: "
            "{'query': msg, 'result': final_answer}"
        ),
        llm=llm,
        can_handoff_to=["addition_agent", "multiplication_agent", "review_agent"],
    )

    workflow = AgentWorkflow(
        agents=[supervisor_agent, review_agent, addition_agent, multiplication_agent],
        root_agent="supervisor_agent",
        initial_state={"fn_call_count": 0},
        state_prompt="Current state: {state}. User message: {msg}",
        early_stopping_method='generate',
    )

    ctx = Context(workflow)

    res = await workflow.run(user_msg="Can you add 3 and 4 and multiply the result by 5?", ctx=ctx)
    print(res)

    #==============================================================================
    # ⚠️ LIMITATION: Token Prediction Bias
    # The code block below will fail or provide incorrect answers. 
    # When an LLM sees standard mathematical notation (e.g., brackets and operators), 
    # its token-prediction engine eagerly attempts to solve the math itself 
    # ("mental math") rather than routing the sub-steps to the proper tool agents. 
    # To handle arbitrary math equations reliably, we must replace granular math 
    # agents with a single agent equipped with a Python REPL execution tool. I will 
    # add a demo for this soon.
    #================================================================================
    #res2 = await workflow.run(user_msg="solve (100 + 10) * 1000", ctx=ctx)
    #print(res2)

    st = await ctx.store.get("state")
    print(f"Total no of function call(s): {st.get('fn_call_count', 'Could not retrieve value')}")

if __name__ == "__main__":
    print("Executing workflow...")
    asyncio.run(main())
    print("done!")