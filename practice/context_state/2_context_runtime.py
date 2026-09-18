from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.tools import tool, ToolRuntime
from langchain.messages import AIMessage
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class UserInfoContext:
    user_name: str
    language: str

@tool
def get_user_info(runtime:ToolRuntime[UserInfoContext]) -> str:
    """Get the current user name"""
    username = runtime.context.user_name
    language = runtime.context.language
    return f""" 
    User name: {username},
    Preferred Language: {language} 
    """

system_prompt = """
You are a science fiction character creator.
When you need information about the current user, use the get_user_info tool.

Create a fictional character profile for the user based on their request.
Use the user's actual name only if they explicitly provide it. Otherwise, use "Unknown" rather than guessing their real name.
Please keep to this structure:

Name:
Language:
Role:
Location:
Faction:
Vibe: 2-3 words
Occupation:
Special Skill:
Personality: 2-3 words
Goal:
Backstory: 1-2 sentences

All details other than information explicitly provided by the user should be treated as fictional and created for the science fiction setting.
"""

llm = ChatOllama(
    model= 'ornith-1.5:9b',
    base_url= os.getenv('SERVER_OLLAMA_BASE_URL'),
    temperature=0.7
)

agent = create_agent(
    model=llm,
    context_schema=UserInfoContext,
    tools=[get_user_info],
    system_prompt=system_prompt
)

context = UserInfoContext(
    user_name = "Jisan",
    language = "Bangla"
)

msg = HumanMessage("What is the user name?")
response = agent.invoke(
    {"messages": [msg]},
    context=context
)

print(response["messages"])
for messages in response["messages"]:
    if isinstance(messages, AIMessage):
        print(messages.content)