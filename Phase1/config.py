import os


class BedrockConfig:
    REGION = os.getenv("BEDROCK_REGION", "us-east-1")

    MODELS = {
        "claude": os.getenv("CLAUDE_MODEL_ID"),
        "embed": os.getenv("TITAN_MODEL_ID"),
    }

    EVALUATE_PROMPT = {
        "promptId": os.getenv("PROMPT_ID"),
        "promptVersion": os.getenv("PROMPT_VERSION"),
    }
