from config import BedrockConfig
from langchain_aws import ChatBedrockConverse
from prompt.translationprompt import get_translation_prompt


class LLMChainService:
    def __init__(self):
        self.config = BedrockConfig()
        # Initialize Bedrock model
        self.model = ChatBedrockConverse(
            model_id=self.config.MODELS["claude"],
            region_name=self.config.REGION,
            temperature=0.7,
            top_p=0.9,
        )

    def run(self, topic: str) -> str:
        prompt = get_translation_prompt()
        chain = prompt | self.model
        for chunk in chain.stream({"input": topic}):
            print(chunk.text, end="|")
        return
