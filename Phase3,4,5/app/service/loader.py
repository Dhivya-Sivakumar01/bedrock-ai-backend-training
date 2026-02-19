from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

def load_documents(path="data"):
    loader = PyPDFDirectoryLoader(path)
    documents = loader.load()

    if not documents:
        raise ValueError("No documents found")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_documents(documents)
