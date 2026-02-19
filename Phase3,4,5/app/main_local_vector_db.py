from service.loader import load_documents
from service.vector_store import create_local_vector_store, load_vector_store, get_retriever
from service.chat_llm import get_llm
from rag import build_rag_chain

def initialize_vector_db():
    docs = load_documents('data')
    create_local_vector_store(docs)
    print("Vector index created.")

def run_chat():
    vectorstore = load_vector_store()
    retriever = get_retriever(vectorstore)
    llm = get_llm()

    rag_chain = build_rag_chain(llm, retriever)

    while True:
        query = input("\nAsk your question (or type exit): ")

        if query.lower() == "exit":
            break

        response = rag_chain.invoke(query)

        print("\nAnswer:\n")
        print(response["answer"])

        print("\nSources:\n")
        for doc in response["docs"]:
            print("-", doc.metadata.get("source", "Unknown"))

if __name__ == "__main__":
    # initialize_vector_db()

    run_chat()
