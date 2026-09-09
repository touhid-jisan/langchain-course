from pprint import pprint
from typing import Any
from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient
import os

from ollama import web_search
load_dotenv()

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)


# print(web_search.invoke("Who is the prime minister of Bangladesh?"))
question = HumanMessage("Who is the prime minister of Bangladesh")

llm = ChatOllama(
    model="ornith-1.5:9b", 
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL"),
    num_ctx=8192
)

search_agent = create_agent(
    model = llm,
    tools= [web_search]
)

response = search_agent.invoke(
    {"messages": [question]}
)

pprint(response['messages'])