from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class UserInfoContext:
    user_name: str
    language: str


llm = ChatOllama(
    model= 'ornith-1.5:9b',
    base_url= os.getenv('SERVER_OLLAMA_BASE_URL')
)


agent = create_agent(
    model=llm,
    context_schema=UserInfoContext
)


context = UserInfoContext(
    user_name = "Jisan",
    language = "English"
)

msg = HumanMessage("What is the user name?")
response = agent.invoke(
    {"messages": [msg]},
    context=context
)

print(response)