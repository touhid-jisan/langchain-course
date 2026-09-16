from langchain.agents import create_agent
import os
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
load_dotenv()
def get_weather(city:str) -> str:
    """Get weather from a given city"""
    return f"Its always sunny in {city}"

llm = ChatOllama(
    model="ornith-1.5:9b",
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL")
)

tools = [get_weather]

agent = create_agent(
    model=llm,
    tools= tools,
    system_prompt="You are a helpful assistant"
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1])
