from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage
import os


load_dotenv()
system_prompt = "You are a science fiction writter. create a capital city at user request."

llm = ChatOllama(
    model= 'ornith-1.5:9b',
    base_url= os.getenv('SERVER_OLLAMA_BASE_URL')
)

scifi_agent = create_agent(
    model = llm,
    system_prompt=system_prompt
)
question = HumanMessage(content="What is the capital of Moon?")

response = scifi_agent.invoke(
    {'message': [question]}
)


print(response['message'][-1].content)