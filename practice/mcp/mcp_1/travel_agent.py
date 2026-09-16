from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from dotenv import load_dotenv
import asyncio
import os


load_dotenv()



async def main():
    client = MultiServerMCPClient(
        {
            "travel_server": {
                "transport": "streamable_http",
                "url": "https://mcp.kiwi.com"
            }
        }
    )


    tools = await client.get_tools()
    
    llm = ChatOllama(
        model="ornith-1.5:9b", 
        base_url=os.getenv("SERVER_OLLAMA_BASE_URL"),
        num_ctx=16384
    )

    travel_agent = create_agent(
        model=llm,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt="You are a travel agent. No follow up question."
    )

    config = {
        "configurable": {"thread_id": "1"}
    }

    msg = HumanMessage(content="Get me a direct flight from San francisco to tokyo on September 30th")

    response = await travel_agent.ainvoke(
        {
            "messages": [msg]
        },
        config=config
    )
    print(response["messages"][-1].content)

if __name__ =="__main__":
    asyncio.run(main())