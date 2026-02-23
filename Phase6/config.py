import os
from dotenv import load_dotenv

load_dotenv()


class BedrockConfig:
    REGION = os.getenv("BEDROCK_REGION", "us-east-1")

    MODELS = {
        "claude": os.getenv("CLAUDE_MODEL_ID"),
        "embed": os.getenv("EMBED_MODEL_ID"),
    }

    EVALUATE_PROMPT = {
        "promptId": os.getenv("PROMPT_ID"),
        "promptVersion": os.getenv("PROMPT_VERSION"),
    }

