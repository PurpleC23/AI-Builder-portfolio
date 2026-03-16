import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv
load_dotenv()

# Load and split PDF
loader = PyPDFLoader("document.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

print(f"✅ Split into {len(chunks)} chunks")

# Free local embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("✅ Embeddings model loaded")

vectorstore = PineconeVectorStore.from_documents(
    chunks,
    embeddings,
    index_name="rag-agent"
)

print("✅ Documents stored in Pinecone!")