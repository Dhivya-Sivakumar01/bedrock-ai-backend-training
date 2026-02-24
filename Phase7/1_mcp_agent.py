# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
import asyncio
from langchain_aws import ChatBedrock
import boto3
from config import BedrockConfig

server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["/Users/dhivyas/Documents/GenAI/AWS GenAI/Training/Phase7/1_mcp_server.py"],
)

bedrock_client = boto3.client(
    service_name="bedrock-runtime", region_name=BedrockConfig.REGION
)



async def main():

    client = MultiServerMCPClient(
    {
        "math": {
            "command": "/Users/dhivyas/Documents/GenAI/AWS GenAI/venv/bin/python",
            "args": ["/Users/dhivyas/Documents/GenAI/AWS GenAI/Training/Phase7/mcp_math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            "command": "/Users/dhivyas/Documents/GenAI/AWS GenAI/venv/bin/python",
            "args": ["/Users/dhivyas/Documents/GenAI/AWS GenAI/Training/Phase7/mcp_weather_server.py"],
            "transport": "stdio",
        }
    })

    tools = await client.get_tools()
    print("Loaded tools:", [t.name for t in tools])

    llm = ChatBedrock(
        model_id=BedrockConfig.MODELS["claude"],
        client=bedrock_client,
        temperature=0.7,
        max_tokens=1024,
    )

    agent = create_agent(model=llm, tools=tools)

    math_response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "what's (3 + 5) x 12?"}
        ]
    })

    weather_response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "what is the weather in nyc?"}
        ]
    })

    print("Math response:", math_response["messages"][-1].content)
    print("Weather response:", weather_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())