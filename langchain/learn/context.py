""" In this module we will demonstrate the langchain's capability of passing context at
    the runtime, and how we can pass on the context to different tools to provide neccassary
    information/context at the runtime, and get the job done.

    `Context`: Context provides immutable run time data which can be passed at invocation time.
               Use it for user IDs, session details, or application-specific settings that
               shouldn’t change during a conversation.
"""
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langchain_core.utils.uuid import uuid7

from langchain.agents import create_agent
from langchain.messages import AIMessage, ToolMessage, HumanMessage

user_id1 = str(uuid7())
user_id2 = str(uuid7())

USER_DB = {
    user_id1: {
        "name": "Tony Stark",
        "account_type": "Premium",
        "balance": 5000,
        "currency": "USD",
        "email": "iamironman@starkindustries.com",
    },
    user_id2: {
        "name": "Pepper Potts",
        "account_type": "Standard",
        "balance": 1200,
        "currency": "USD",
        "email": "pepper@starkindustries.com",
    },
}

@dataclass
class User():
    user_id: str

llm = init_chat_model('ollama:gemma4:12b-mlx')

@tool("get_user_info", description="fetch user account information from database.")
def get_user_info(runtime: ToolRuntime[User]):
    """Get the current user's account information."""
    user_id = runtime.context.user_id
    if user_id in USER_DB:
        user = USER_DB[user_id]
        return user

    return "User not found"

agent = create_agent(model=llm, tools=[get_user_info], context_schema=User)

while True:
    try:
        ques = input("Please type in your question or press 'q' to exit...\n")
        if str(ques) == 'q':
            print("Exiting...")
            break
        response = agent.invoke(
            { "messages": [{ "role": "user", "content": ques}]},
            config={"configurable": { "thread_id": str(uuid7())}},
            context=User(user_id=user_id2)
        )

        for message in response["messages"]:
            if isinstance(message, HumanMessage):
                pass
                # print(f"User: {message.text}")
            if isinstance(message, AIMessage):
                print(message.text, end="\n\n>")
            if isinstance(message, ToolMessage):
                print(f"[tool used: {message.name}] \n")

    except Exception:
        break
