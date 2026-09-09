from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from dotenv import load_dotenv
import os

load_dotenv()


# # if we want the Python function name and tool name to be different:
# @tool("square_rootx")
# def tool1(value:float) -> float:
#     """Calculate the square root of a number"""
#     return value ** 0.5


# # when we specifically want to define the tool description separately:
# @tool(
#     "square_root",
#     description="Calculate the square root of a number."
# )
# def calculate(x: float) -> float:
#     return x ** 0.5

@tool
def square_root(value:float) -> float:
    """Calculate the square root of a number"""
    return value ** 0.5

@tool
def square(value: float) -> float:
    """Calculate the square of a number"""
    return value ** 2

system_prompt="""
    You are an arithmetic assistant.

    When the user asks to first find the square root
    and then square the result:
    
    1. Call square_root first.
    2. Take the result of square_root.
    3. Pass that result to square.
    4. Return the final result.
"""

llm = ChatOllama(
    model="ornith-1.5:9b", 
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL")
)

agent = create_agent(
    model=llm,
    tools=[square_root, square],
    system_prompt=system_prompt

)
question1 = HumanMessage("What is the square root of 49.5? then square the result")

response = agent.invoke(
    {'messages': [question1]}
)

print(response['messages'][-1].content)

for msg in response['messages']:
    print(msg)

