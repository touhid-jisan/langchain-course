from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.messages import HumanMessage 
from dotenv import load_dotenv
import os

load_dotenv()

system_prompt = """
You are a science fiction writer, create a space capital city at the users request.
Please keep to the below structure.
Name: The name of the capital city
Location: Where it is based
Vibe: 2-3 words to describe its vibe
Economy: Main industries
"""

llm = ChatOllama(
    model="ornith-1.5:9b", 
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL")
)

scifi_agent = create_agent(
    model=llm,
    system_prompt=system_prompt
)

question = HumanMessage(content="What's the capital of the moon?")

response = scifi_agent.invoke(
    {'messages': [question]}
)

print(response['messages'][1].content)