import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openrouter import ChatOpenRouter
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

load_dotenv()

# @tool
# def search_on_internet(query: str) -> str:
#     """
#     Tool that searches over internet
#     Args:
#         query: The query to search for

#     Returns:
#         The search result
#     """
#     print(f"Searching for {query}\n")
#     return tavily.search(query=query)

class Source(BaseModel):
    """Schema for a source used by the agent"""

    url: str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer: str = Field(description="Thr agent's answer to the query")
    sources: List[Source] = Field(
        default_factory=list, description="List of sources used to generate the answer"
    )

llm = ChatOllama(
    model = "llama3.1:8b",
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL"),
    temperature=0
)


tools = [TavilySearch(
    start_date="2026-01-01",
    end_date="2026-08-20"
)]

agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():
    # result = agent.invoke({"messages": HumanMessage(content="What is the weather in Tokyo righ now")})
    # result = agent.invoke(
    #     {"messages": HumanMessage(content="What is the weather in Tokyo righ now")}
    # )

    result = agent.invoke(
        {
            "messages": HumanMessage(
                content="search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details?"
            )
        }
    )

    print(result)
    # print(result['structured_response'])
    # print(result['structured_response'].answer)

    print("Available keys:", result.keys())
if __name__ == "__main__":
    main()
