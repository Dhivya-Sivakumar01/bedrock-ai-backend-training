from langchain_core.prompts import ChatPromptTemplate

def get_translation_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that translates English to French."),
        ("human", "{input}")
    ])