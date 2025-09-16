import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


def _load_pdf(path: str):
    loader = PyPDFLoader(path)
    return loader.load()


def create_pdf_agent_from_files(pdf_paths: list):
    all_docs = []
    for path in pdf_paths:
        all_docs.extend(_load_pdf(path))
    docs = all_docs
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    embeddings = GoogleGenerativeAIEmbeddings(model="embedding-001", google_api_key=api_key)
    vectordb = FAISS.from_documents(chunks, embedding=embeddings)
    retriever = vectordb.as_retriever()

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=api_key)

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
    )

def create_pdf_agent(pdf_path: str):
    return create_pdf_agent_from_files([pdf_path])
