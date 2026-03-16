# AI Builder Portfolio

A collection of practical, production-ready AI projects built with Python, LangChain, Ollama, Groq, and n8n. Each project solves a real problem and is built to production standards — not just tutorials.

---

## Projects

### 1. [JobReady — AI Job Hunting Assistant](./jobready-ai)
An AI-powered job hunting assistant that takes you from "I need a job" to "I'm ready to apply" in minutes.

- 6 features: Resume parsing, job search with salary ranges, job analyzer, cover letter generator, interview prep, ATS optimizer
- 13+ job boards including LinkedIn, RemoteOK, Wellfound, Reddit, Naukri
- Auto-logs every application to Airtable
- Built with Python, Streamlit, Groq, BeautifulSoup, fpdf2, Airtable
- [View README](./jobready-ai/README.md)

---

### 2. [RAG Support Agent](./rag-support-agent)
A document Q&A agent that answers questions from any PDF using Retrieval Augmented Generation.

- Zero hallucinations — only answers from your document
- Shows source chunks used for every answer
- Query logging via n8n + Airtable
- Built with Python, LangChain, Pinecone, HuggingFace, Ollama, Streamlit
- [View README](./rag-support-agent/README.md)

---

### 3. [AI Productivity Assistant](./ai-productivity-assistant)
An automated productivity system that converts natural language into structured tasks and calendar events.

- Production-grade: error handling, duplicate detection, webhook trigger
- Duplicate detection — queries Notion before creating tasks, prevents database pollution
- Tasks go to Notion, meetings go to Google Calendar — automatically
- Built with n8n, Groq, Notion API, Google Calendar API
- [View README](./ai-productivity-assistant/README.md) • [Import Workflow](./ai-productivity-assistant/workflow.json)

---

## Tech Stack Across Projects

Python • LangChain • Groq • Ollama • Streamlit • n8n • Airtable • Pinecone • BeautifulSoup • HuggingFace

---

## About

Self-taught AI developer building practical tools that solve real problems. Currently completing CS50 Python and CS50 AI.

[GitHub](https://github.com/PurpleC23) • [LinkedIn](https://linkedin.com/in/chahal-tilak-a248a9271)