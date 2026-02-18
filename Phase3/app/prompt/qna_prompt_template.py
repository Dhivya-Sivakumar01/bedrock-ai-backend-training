from langchain_core.prompts import ChatPromptTemplate

def get_qna_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", '''You are a Question Answering AI assistant.
                Answer strictly based on the provided context.
                Do not use prior knowledge.
                Do not make hallucinate.
                If the answer is not explicitly present in the context, respond exactly with:"I don't know based on the provided documents.
         When answering, mention the source file names in brackets like [source.pdf]."'''),
        ("human", '''<context>
                {context}
                </context>

                Question:
                {input}

                Provide a detailed answer (minimum 250 words).''')
    ])