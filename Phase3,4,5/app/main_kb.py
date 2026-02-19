import boto3
import os
from config import BedrockConfig
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from rag import build_rag_chain_kb
from service.chat_llm import get_llm

REGION = BedrockConfig.REGION
KNOWLEDGE_BASE_ID = BedrockConfig.KNOWLEDGE_BASE['knowledge_base_id']

# Create Bedrock Agent Runtime client
bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=REGION
)
retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=KNOWLEDGE_BASE_ID,
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},
)

def kb_retrieve(query):
    llm = get_llm()
    rag_chain = build_rag_chain_kb(llm, retriever)

    while True:
        query = input("\nAsk your question (or type exit): ")

        if query.lower() == "exit":
            break

        response = rag_chain.invoke(query)

        print("\nAnswer:\n")
        print(response)

        # print("\nSources:\n")
        # for doc in response["docs"]:
        #     print("-", doc.metadata.get("source", "Unknown"))


if __name__ == "__main__":
    request = input("Enter your question")
    kb_retrieve(request)

# Benefits of credit card
