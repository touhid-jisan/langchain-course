import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama

load_dotenv()
system_prompt = """

You are a science fiction writer, create a space capital city at the users request.

User: What is the capital of mars?
Scifi Writer: Marsialis

User: What is the capital of Venus?
Scifi Writer: Venusovia

"""
question = HumanMessage(content="What is the capital of Moon?")

llm = ChatOllama(
    model="ornith-1.5:9b", 
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL")
)

scifi_agent = create_agent(
    model=llm, 
    system_prompt=system_prompt
)

response = scifi_agent.invoke(
    {"messages": [question]}
)

print(response["messages"][1].content)
