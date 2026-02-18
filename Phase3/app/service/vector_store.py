import boto3
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
from langchain_aws import ChatBedrockConverse
from config import BedrockConfig


bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=BedrockConfig.REGION
)

embedding_client = BedrockEmbeddings(
    model_id=BedrockConfig.MODELS['embed'],
    client=bedrock_client
)
def create_vector_store(docs):
    vectorstore = FAISS.from_documents(docs, embedding_client)
    vectorstore.save_local("faiss_index")
    return vectorstore

def get_retriever(vectorstore):
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

def load_vector_store():
    return FAISS.load_local(
        "faiss_index",
        embedding_client,
        allow_dangerous_deserialization=True
    )
