import asyncio
from strands import Agent
from strands.tools.mcp import MCPClient
from config import BedrockConfig
from mcp import stdio_client, StdioServerParameters
from mcp.types import ElicitResult

# Use your venv python path here
PYTHON_PATH = BedrockConfig.PYTHON_PATH

async def elicitation_callback(context, params):
    print(f"ELICITATION: {params.message}")
    # Get user confirmation...
    return ElicitResult(
        action="accept",
        content={"username": "myname"}
    )

async def main():

    mathServer = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(command=PYTHON_PATH, args=[BedrockConfig.MCP_PATH+"/mcp_math_server.py"],)
        ),
        elicitation_callback=elicitation_callback,
    )

    weatherServer = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(command=PYTHON_PATH, args=[BedrockConfig.MCP_PATH+"/mcp_weather_server.py"],)
        ),
        elicitation_callback=elicitation_callback,
    )
    with mathServer, weatherServer:
        tools = mathServer.list_tools_sync() + weatherServer.list_tools_sync()
        print("Tools listed: ",tools)

        agent = Agent(
            name="strandsMCPAgent",
            model=BedrockConfig.MODELS["claude"],
            tools=tools
        )
        print(dir(agent))

        math_result = await agent.invoke_async("what's (3 + 5) x 12?")
        weather_result = await agent.invoke_async("what is the weather in nyc?")
        print("\nMath Result:", math_result)
        print("\nWeather Result:", weather_result)

if __name__ == "__main__":
    asyncio.run(main())