import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    client = MultiServerMCPClient(
        {
            "local_server": {
                "transport": "stdio",
                "command": "python",
                "args": ["mcp_server.py"],
            }
        }
    )

    tools = await client.get_tools()

    print(tools)


if __name__ == "__main__":
    asyncio.run(main())