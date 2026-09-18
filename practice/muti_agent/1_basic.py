from langchain import tools
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

from urllib3 import response

load_dotenv()

@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    return x**0.5


@tool
def square(x: float) -> float:
    """Calculate the square of a number"""
    return x**2


llm = ChatOllama(
    model= 'ornith-1.5:9b',
    base_url= os.getenv('SERVER_OLLAMA_BASE_URL'),
)

subagent_1 = create_agent(
    model= llm,
    tools=[square_root]
)

subagent_2 = create_agent(
    model= llm,
    tools=[square],
)

@tool
def call_subagent_1(x:float) -> float:
    """Call subagent 1 in order to calculate the square root of a number."""
    response = subagent_1.invoke(
        {"messages": [HumanMessage(content=f"Calculate the square root of {x}")]}
    )
    return response["messages"][-1].content


@tool
def call_subagent_2(x:float) -> float:
    """Call subagent 2 in order to calculate the square of a number."""
    response = subagent_2.invoke(
        {"messages": [HumanMessage(content=f"Calculate the square of {x}")]}
    )
    return response["messages"][-1].content


main_agent = create_agent(
    model=llm,
    tools=[call_subagent_1, call_subagent_2],
    system_prompt="You are a helpful assistant who can call subagents to calculate the square root or square of a number."
)

response = main_agent.invoke(
    {"messages": [HumanMessage(content="What is the square root of 456 and square of 10")]}
)

print(response["messages"][-1].content)