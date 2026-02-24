import os
from dotenv import load_dotenv

load_dotenv()


class BedrockConfig:
    REGION = os.getenv("BEDROCK_REGION", "us-east-1")

    MODELS = {
        "claude": os.getenv("CLAUDE_MODEL_ID"),
        "embed": os.getenv("EMBED_MODEL_ID"),
    }

    PYTHON_PATH = os.getenv("PYTHON_PATH")

    MCP_PATH = os.getenv("MCP_PATH")

