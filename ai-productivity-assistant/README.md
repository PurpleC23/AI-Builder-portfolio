#  AI Productivity Assistant

**[Watch Demo](https://youtu.be/jer4Ofldt1g)**

An AI-powered automation system that converts natural language text into structured tasks and calendar events. Zero manual effort — just describe what needs to be done.

---

## The Problem

Professionals write tasks inside messages, emails, and notes every day:

> *"Prepare Q3 marketing report by Friday and schedule meeting with design team next week."*

Manually moving these into task managers and calendars is time-consuming and error-prone. This system does it automatically.

---

## How It Works — The Flow
```
Webhook receives text input
        ↓
Groq LLM extracts structured JSON
(task name, type, date, priority, category, source)
        ↓
JavaScript validates the JSON output
        ↓
Error handler catches bad AI responses → logs to Notion
        ↓
Tasks split into individual items
        ↓
Notion queried for duplicate detection
(Task ID = slug + date)
        ↓
Each item categorized: task or meeting?
        ↓
Tasks → Notion database
Meetings → Google Calendar
```

---

## What Makes This Production-Grade

Most automation tutorials show happy-path demos. This system is built for the real world:

- **Error handling** — if the LLM returns malformed JSON, the workflow catches it, logs the raw output to Notion, and exits cleanly. No silent failures.
- **Duplicate detection** — before creating any task, the system queries Notion using a unique Task ID (slug + date). If it already exists, it skips. Your database stays clean.
- **Webhook trigger** — the system isn't a manual button click. It's a real API endpoint that can be called from any app, Slack bot, email parser, or form.
- **Data merge node** — preserves original task metadata (category, priority, source) across API calls so nothing gets lost between nodes.
- **Observability** — every error is logged with timestamp, error type, and raw AI output so debugging is always possible.

---

## Key Features

- **Natural language input** — send any text, AI figures out the rest
- **Duplicate detection** — checks Notion before creating, prevents pollution
- **Error handling** — bad AI output is caught, logged, never silently fails
- **Smart routing** — tasks and meetings go to different systems automatically
- **Webhook trigger** — can be called from any app, form, or automation
- **Date fallback** — if no date extracted, defaults to today

---

## Example

**Input:**
```json
{
  "text": "Prepare Q3 marketing report by Friday and schedule meeting with design team next week."
}
```

**Output:**
- ✅ Notion task created: `Prepare Q3 marketing report` — Priority: High — Due: Friday
- ✅ Google Calendar event created: `Meeting with design team` — Next week

---

## Tech Stack

| Tool | Purpose |
|---|---|
| n8n | Workflow orchestration |
| Groq (Llama 3.1) | Natural language task extraction |
| JavaScript | JSON validation + Task ID generation |
| Notion API | Task database |
| Google Calendar API | Meeting scheduling |

---

## Setup

1. Import `workflow.json` into your n8n instance
2. Add your credentials:
   - Groq API key
   - Notion API key + Database ID
   - Google Calendar OAuth
3. Activate the webhook
4. Send a POST request to the webhook URL:
```json
{
  "text": "your task or meeting description here"
}
```

---

## Project Structure
```
ai-productivity-assistant/
│
├── workflow.json     # n8n workflow — import directly into n8n
└── README.md
```

---

## Screenshots

*Workflow diagram, Notion task database, and Google Calendar output — see demo video.*

---

## Built By

Chahal Tilak — Self-taught AI developer building practical AI tools.

[GitHub](https://github.com/PurpleC23) • [LinkedIn](https://linkedin.com/in/chahal-tilak-a248a9271)