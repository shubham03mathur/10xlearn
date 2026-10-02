from langchain.messages import AIMessage, HumanMessage
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model

llm = init_chat_model('ollama:gemma4:12b-mlx')

@tool('get_user_info')
def get_user_info(user_id: str , runtime: ToolRuntime) -> str:
    """ get user info from store/memory """
    store = runtime.store
    if store:
        user = store.get(('users', ), user_id)
        return str(user.value) if user else "no user found"
    else:
        return "could't retrieve the user info. Please verify the details again."

@tool('save_user_info')
def set_user_info(user_id: str, name: str, age: int, email: str, runtime: ToolRuntime) -> str:
    """ save user info/data to store/memory """
    store = runtime.store
    if store:
        store.put(('users,', ), user_id, { "name": name, "age": age, "email": email})
        return "successfull saved user info"
    else:
        return "couldn't save the user info. Please try again."

store = InMemoryStore()
agent  = create_agent(model=llm, tools=[get_user_info, set_user_info], store=store)

response = agent.invoke({
    "messages": [HumanMessage('Save the following user: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev')]
})

for message in response["messages"]:
    if isinstance(message, AIMessage):
        print(message.text, "\n\n")

response = agent.invoke({
    "messages": [{"role": "user", "content": "Get user info for user with id abc123"}]
})

for message in response["messages"]:
    if isinstance(message, AIMessage):
        print(message.text, "\n\n")