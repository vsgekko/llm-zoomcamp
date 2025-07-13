import asyncio
from fastmcp import Client
from weather_server import mcp      # your FastMCP instance

async def main():
    async with Client(mcp) as client:
        tools = await client.list_tools()
        #print("Available tools:", tools)
        print(tools)
        #resp = await client.call_tool("get_weather", {"city": "Berlin"})
        #print("Berlin temperature:", resp.data)

if __name__ == "__main__":
    asyncio.run(main())
