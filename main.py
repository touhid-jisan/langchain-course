from dotenv import load_dotenv

load_dotenv()
import os

from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
# from langchain import hub
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langchain_core.output_parsers.pydantic import PydanticOutputParser  

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTION
from schemas import AgentResponse


tools = [TavilySearch()]

llm = ChatOllama(
    model="llama3.2",
    # base_url=os.getenv("SERVER_OLLAMA_BASE_URL"),
    temperature=0,
)
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

react_pormpt_with_format_istructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTION,
    input_variables=["input", "agent_scratchpad", "tool_names"]
).partial(format_instructions = output_parser.get_format_instructions())

agent = create_react_agent(
    llm=llm, 
    tools=tools, 
    prompt=react_pormpt_with_format_istructions)

agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)
chain = agent_executor


def main():
    result = chain.invoke(
        input={
            "input": "search for 3 job posting for an ai engineer using langchain in the bay area on linkedin and list their details."
        }
    )

    print(result)


if __name__ == "__main__":
    main()
