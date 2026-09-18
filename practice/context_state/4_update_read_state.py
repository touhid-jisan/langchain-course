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

@tool
def read_favourite_color(runtime: ToolRuntime) -> str:
    """Read the favourite color of the user from the state."""
    try:
        return runtime.state["favourite_color"]
    except KeyError:
        return "No favourite color found in the state."

llm = ChatOllama(
    model= 'ornith-1.5:9b',
    base_url= os.getenv('SERVER_OLLAMA_BASE_URL'),
)

agent = create_agent(
    model= llm,
    checkpointer=InMemorySaver(),
    tools= [update_favourite_color, read_favourite_color],
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


response = agent.invoke(
    { 
        "messages": [HumanMessage(content="Hello, how are you? my favourite color is now green. update it.")],
    },
    {"configurable": {"thread_id": 1}}
)

print(response)

response = agent.invoke(
    { 
        "messages": [HumanMessage(content="Hello, what's my favourite color?")]
    },
    {"configurable": {"thread_id": 1}}
)
print(response)