import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from logger import log_to_n8n

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="NovaTech Support Agent", page_icon="🤖")
st.title("🤖 NovaTech AI Support Agent")
st.caption("Powered by RAG — answers grounded in official documentation.")

@st.cache_resource
def load_chain():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = PineconeVectorStore(index_name="rag-agent", embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = Ollama(model="mistral")

    prompt = PromptTemplate.from_template("""You are a helpful customer support agent for NovaTech Solutions.
Use the following document excerpts to answer the question accurately and concisely.
If the answer is not in the documents, say "I don't have that information in my knowledge base."

Context:
{context}

Question: {question}

Answer:""")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever

chain, retriever = load_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if question := st.chat_input("Ask anything about NovaTech..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            answer = chain.invoke(question)
            sources = retriever.invoke(question)

        st.write(answer)

        with st.expander("📄 Sources used"):
            for i, doc in enumerate(sources):
                page = doc.metadata.get("page", "unknown")
                st.markdown(f"**Chunk {i+1} (Page {page}):**")
                st.caption(doc.page_content[:300] + "...")

        log_to_n8n(question, answer, sources)

    st.session_state.messages.append({"role": "assistant", "content": answer})