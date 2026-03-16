#  RAG Support Agent

An AI-powered document Q&A agent built with RAG (Retrieval Augmented Generation). Upload any PDF — ask questions — get accurate answers grounded in the document. Zero hallucinations, zero ongoing API costs.

---

## What It Does

Most AI chatbots make up answers when they don't know something. This one can't — it only responds using content from your actual document. Built as a customer support agent for NovaTech Solutions (a fictional B2B SaaS company), but works with any PDF.

---

## How It Works — The Flow
```
Your PDF Document
      ↓
Split into 500-word chunks
      ↓
HuggingFace converts each chunk into a vector (embedding)
      ↓
Vectors stored in Pinecone (vector database)
      ↓
User asks a question
      ↓
Question converted to vector → top 3 matching chunks retrieved
      ↓
Chunks + question sent to Mistral (local LLM via Ollama)
      ↓
Grounded answer generated — only from your document
      ↓
Answer + sources displayed in Streamlit UI
      ↓
Query and response logged to Airtable via n8n webhook
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| LangChain | RAG pipeline orchestration |
| Pinecone | Vector database for semantic search |
| HuggingFace (all-MiniLM-L6-v2) | Free local embeddings |
| Ollama + Mistral 7B | Free local LLM — no API costs |
| Streamlit | Chat UI |
| n8n + Airtable | Query logging and observability |

---

## Why RAG?

Standard LLMs hallucinate — they confidently make up answers. RAG fixes this by forcing the model to answer only from retrieved document chunks. The UI shows exactly which document sections were used to generate each answer so every response is traceable and verifiable.

---

## Key Features

- **Source transparency** — every answer shows which document chunks were used
- **Any PDF** — swap the document and it works for any use case
- **Zero hallucinations** — if the answer isn't in the document, it says so
- **Observability** — every query and response logged to Airtable via n8n
- **Free to run** — local embeddings + local LLM = zero API costs

---

## Setup & Installation

**Requirements:**
- Python 3.10+
- Ollama installed with Mistral pulled
- Pinecone account (free tier works)

**Steps:**
```bash
# Clone the repo
git clone https://github.com/PurpleC23/AI-Builder-portfolio.git
cd AI-Builder-portfolio/rag-support-agent

# Install dependencies
pip install -r requirements.txt

# Add your keys to .env
PINECONE_API_KEY=your_key_here

# Ingest your PDF
python ingest.py

# Launch the chat UI
streamlit run app.py
```

---

## Project Structure
```
rag-support-agent/
│
├── app.py          # Streamlit chat UI + RAG chain
├── ingest.py       # PDF ingestion + Pinecone storage
├── chat.py         # Terminal version of the agent
├── logger.py       # n8n webhook logging
├── document.pdf    # Sample document (NovaTech FAQ)
└── requirements.txt
```

---

## Built By

Chahal Tilak — Self-taught AI developer building practical AI tools.

[GitHub](https://github.com/PurpleC23) • [LinkedIn](https://linkedin.com/in/chahal-tilak-a248a9271)