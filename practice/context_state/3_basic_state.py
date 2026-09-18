from langchain.agents import create_agent, AgentState
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
from langgraph.types import Command
from dotenv import load_dotenv
import os

load_dotenv()


class CustomState(AgentState):
    favourite_color: str

@tool
def update_favourite_color(favourite_color: str, runtime: ToolRuntime) -> Command:
    """Update the favourite color of the user in the state once they've revealed it."""
    return Command(
        update= {
            "favourite_color": favourite_color,
            "messages": [ToolMessage("Successfully updated favourite color.", tool_call_id=runtime.tool_call_id)]
        }
    )

llm = ChatOllama(
    model= 'ornith-1.5:9b',
    base_url= os.getenv('SERVER_OLLAMA_BASE_URL'),
)

agent = create_agent(
    model= llm,
    checkpointer=InMemorySaver(),
    tools= [update_favourite_color],
    state_schema= CustomState
)

response = agent.invoke(
    {
        "messages": [HumanMessage("My favourite color is blue.")]
    },
    {
        "configurable": {"thread_id": 1}
    }
)

print(response["favourite_color"])

response = agent.invoke(
    {
        "messages": [HumanMessage("Hello How are you?")],
        "favourite_color": "black"
    },
    {
        "configurable": {"thread_id": 10}
    }
)

print(response["favourite_color"])

response = agent.invoke(
    {
        "messages": [HumanMessage("Whats my favourite color?")],
    },
    {
        "configurable": {"thread_id": 1}
    }
)
print(response)