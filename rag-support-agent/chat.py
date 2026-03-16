import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

os.environ["PINECONE_API_KEY"] = "your_pinecone_key_here"

# Load embeddings + connect to Pinecone
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = PineconeVectorStore(index_name="rag-agent", embedding=embeddings)

# Free local LLM
llm = Ollama(model="mistral")

# Build RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

print("✅ RAG Agent ready! Ask me anything about your document.")
print("Type 'exit' to quit\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break
    answer = qa_chain.invoke(question)
    print(f"\nAgent: {answer['result']}\n")