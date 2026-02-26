from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models import BedrockModel
from config import BedrockConfig
from datetime import datetime
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from mcp.client.sse import sse_client

MEM_ID = BedrockConfig.AGENTCORE_MEMORY_ID
ACTOR_ID = "test_actor_id_%s" % datetime.now().strftime("%Y%m%d%H%M%S")
SESSION_ID = "test_session_id_%s" % datetime.now().strftime("%Y%m%d%H%M%S")

def create_agent():
    agentcore_memory_config = AgentCoreMemoryConfig(
        memory_id=MEM_ID,
        session_id=SESSION_ID,
        actor_id=ACTOR_ID,
        batch_size=5,
    )

    mcp_client = MCPClient(lambda: sse_client("http://localhost:3000/sse"))

    llm = BedrockModel(
        model_id=BedrockConfig.MODELS["claude"],
        region_name=BedrockConfig.REGION,
        temperature=0.7,
        max_tokens=1024,
    )
    session_manager = AgentCoreMemorySessionManager(
        agentcore_memory_config=agentcore_memory_config,
        region_name=BedrockConfig.REGION
    )

    agent = Agent(
        model=llm,
        tools=[mcp_client],
        session_manager=session_manager,
        system_prompt="""
            You are an Employee Management Assistant.

            Rules:
            - Role must be 'Engineer' or 'Associate Engineer'.
            - Always use tools for CRUD.
            - If user refers to employee by name, resolve ID first.
            - If user says 'him' or 'her', use last referenced employee.
            - If questions not related to Employee management, say 'I'm an Employee Management Assistant, can provide info other than Employee topics'
            """
    )

    return agent, session_manager
