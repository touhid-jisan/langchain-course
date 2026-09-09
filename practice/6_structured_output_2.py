from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class CapitalInfo(BaseModel):
    name: str
    location: str
    vibe: str
    economy: str

system_prompt="You are a science fiction writer, create a capital city at the users request."
question = HumanMessage(content="What is the capital of Moon?")

llm = ChatOllama(
    model="ornith-1.5:9b", 
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL")
)

scifi_agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    response_format=CapitalInfo
)

response = scifi_agent.invoke(
    {'messages': [question]}
)

print(response["structured_response"])
print(response["structured_response"].name)
print(response["structured_response"].location)
print(response["structured_response"].vibe)
print(response["structured_response"].economy)