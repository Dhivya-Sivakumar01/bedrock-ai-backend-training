from service.llmchain import LLMChainService

if __name__ == "__main__":
    service = LLMChainService()
    response = service.run("I love programming. Creating applications that can summarize and analyze data from internal documents stored in Amazon S3 using services like Amazon Textract for text extraction.")
    print(response)
