from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from prompt.qna_prompt_template import get_qna_prompt
from langchain_core.prompts import ChatPromptTemplate

prompt = get_qna_prompt()

def build_rag_chain(llm, retriever):
    # Step 1: Retrieve documents
    def retrieve_docs(question):
        docs = retriever.invoke(question)
        return {
            "input": question,
            "docs": docs,
            "context": "\n\n".join(doc.page_content for doc in docs)
        }

    # Step 2: Generate answer
    def generate_answer(inputs):
        response = llm.invoke(
            prompt.invoke({
                "context": inputs["context"],
                "input": inputs["input"]
            })
        )
        return {
            "answer": response.content,
            "docs": inputs["docs"]
        }

    # Step 3: Combine into pipeline
    rag_chain = RunnablePassthrough() | retrieve_docs | generate_answer

    return rag_chain



def build_rag_chain_kb(llm, retriever):
    chain = (
        {"context": retriever, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain