import os
from dotenv import load_dotenv

load_dotenv()


class BedrockConfig:
    REGION = os.getenv("BEDROCK_REGION", "us-east-1")

    MODELS = {
        "claude": os.getenv("CLAUDE_MODEL_ID"),
    }

    AGENTCORE_MEMORY_ID = os.getenv("AGENTCORE_MEMORY_ID")


