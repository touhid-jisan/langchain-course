from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

msg = HumanMessage(content="Hi my name is touhid, my favourite color is blue.")
config = {"configurable": {"thread_id": 1}}

llm = ChatOllama(
    model="ornith-1.5:9b", 
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL")
)

agent = create_agent(
    model=llm,
    checkpointer=InMemorySaver()
)

response = agent.invoke(
    {"messages": [msg]},
    config=config
)

print(response)

response = agent.invoke(
    {"messages": ["what's my favourite color?"]},
    config=config
)

print(response)