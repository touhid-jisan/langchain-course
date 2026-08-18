import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_openrouter import ChatOpenRouter
from tavily import TavilyClient

load_dotenv()
tavily = TavilyClient()


@tool
def search_on_internet(query: str) -> str:
    """
    Tool that searches over internet
    Args:
        query: The query to search for

    Returns:
        The search result
    """
    print(f"Searching for {query}\n")
    return tavily.search(query=query)


llm = ChatOpenRouter(
    model="google/gemma-4-26b-a4b-it:free",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# llm = ChatOllama(
#     model = "qwen2.5-coder:7b"
# )
tools = [search_on_internet]
agent = create_agent(model=llm, tools=tools)


def main():
    # result = agent.invoke({"messages": HumanMessage(content="What is the weather in Tokyo righ now")})
    # result = agent.invoke(
    #     {"messages": HumanMessage(content="What is the weather in Tokyo righ now")}
    # )

    result = agent.invoke(
        {"messages": HumanMessage(content="search for 3 job posting for ai engineer using langchain in the bay area on linkedin and list the details")}
    )
    print(result)


if __name__ == "__main__":
    main()
