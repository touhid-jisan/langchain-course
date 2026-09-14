from typing import Any
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from tavily import TavilyClient

from dotenv import load_dotenv
import os

load_dotenv()
tavily_client = TavilyClient()

def search_recipe(query: str) -> dict[str, Any]:
    """Search the web for information"""
    tavily_client.search(query=query)


system_prompt = """

You are a personal chef. The user will give you a list of ingredients they have left over in their house.

Using the web search tool, search the web for recipes that can be made with the ingredients they have.

Return recipe suggestions and eventually the recipe instructions to the user, if requested.

"""

llm = ChatOllama(
    model="ornith-1.5:9b", 
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL"),
    num_ctx=8192
)

chef_agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    tools=[search_recipe],
    checkpointer=InMemorySaver()
)

config = {"configurable": {"thread_id":1}}
question = HumanMessage(content="Here are the ingredients I have: chicken, rice, onions, and eggs. What recipes can I make?")

response = chef_agent.invoke(
    {"messages": [question]},
    config=config
)

print(response)