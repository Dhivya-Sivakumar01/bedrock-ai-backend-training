from config import BedrockConfig
import boto3
from langchain_aws import BedrockEmbeddings
from langchain_aws import ChatBedrock

bedrock_client = boto3.client(
    service_name="bedrock-runtime", region_name=BedrockConfig.REGION
)

embedding_client = BedrockEmbeddings(
    model_id=BedrockConfig.MODELS["embed"], client=bedrock_client
)


def get_llm():
    return ChatBedrock(
        model_id=BedrockConfig.MODELS["claude"],
        client=bedrock_client,
        temperature=0.7,
        max_tokens=1024,
    )
