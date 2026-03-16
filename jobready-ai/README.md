#  JobReady — AI Job Hunting Assistant

An AI-powered job hunting assistant built with Python, Streamlit, and Groq. Goes from "I need a job" to "I'm ready to apply" in minutes — free, fast, and powered by Groq's lightning-fast LLM API.

---

## What It Does

JobReady is a 6-feature app that guides you through the entire job application process:

1. **Resume Parser** — Upload your resume once (PDF or DOCX). Groq reads it and extracts your skills, experience, and education into a clean structured format. Every other feature uses this automatically.

2. **Job Search** — Based on your parsed resume, Groq suggests the best job titles for your profile with salary ranges for your market. Generates direct search links to 13+ job boards including LinkedIn, Indeed, RemoteOK, Wellfound, WeWorkRemotely, Reddit, Naukri and more.

3. **Job Analyzer** — Paste any job posting URL. JobReady scrapes the page using BeautifulSoup, strips out noise, and sends the job description + your resume to Groq. You get a match score out of 100, your strong matches, your gaps, and an honest verdict.

4. **Cover Letter Generator** — Using your resume and the scraped job description, Groq writes a tailored 3-paragraph cover letter specific to that company and role. No generic templates. Downloadable as PDF.

5. **Interview Prep** — Groq predicts 20 likely interview questions based on the job description and your background. Each question comes with why interviewers ask it and a tailored answer framework using your actual projects and experience.

6. **ATS Optimizer** — Two modes: Generic (optimize resume for any job title) or Specific (optimize against an actual job description). Get your ATS score, missing keywords, optimized summary, and actionable tips. Downloadable report.

Every analyzed job is automatically logged to Airtable as a job application tracker — with match score, job URL, company, and cover letter saved for reference.

---

## How It Works — The Flow
```
Your Resume (PDF/DOCX)
        ↓
  Groq extracts skills, experience, education
        ↓
    ┌─────────────────────────────────────┐
    │                                     │
    ▼                                     ▼
Job Search                          Job Analyzer
(suggests roles + salary ranges     (paste any URL →
+ 13 board links)                   BeautifulSoup scrapes it)
                                          ↓
                                   Match Score (X/100)
                                   Strong Matches
                                   Gaps identified
                                          ↓
                    ┌─────────────────────────────────┐
                    │                 │               │
                    ▼                 ▼               ▼
          Cover Letter          Interview Prep    ATS Optimizer
          (tailored PDF)       (20 predicted     (keywords +
                                Q&A)              ATS score)
                    ↓
             Download as PDF
                    ↓
          Auto-logged to Airtable
          (Job Title, Company, Score,
           Cover Letter, Status)
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| Groq (Llama 3.1) | AI brain — free and fast |
| BeautifulSoup + lxml | Job page scraping |
| fpdf2 | PDF export |
| Airtable API | Job application tracking |
| python-docx + pypdf | Resume file parsing |

---

## Why Groq?

- ✅ Completely free tier — no credit card needed
- ✅ Faster than OpenAI — responses in seconds
- ✅ Llama 3.1 8B — powerful enough for all features
- ✅ Simple API — drop-in replacement for any LLM

---

## Setup & Installation

**Requirements:**
- Python 3.10+
- Groq API key (free at groq.com)

**Steps:**
```bash
# Clone the repo
git clone https://github.com/PurpleC23/AI-Builder-portfolio.git
cd AI-Builder-portfolio/jobready-ai

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your keys to .env
GROQ_API_KEY=your_groq_key_here
AIRTABLE_TOKEN=your_airtable_token_here
BASE_ID=your_airtable_base_id_here

# Run the app
streamlit run app.py
```

---

## Project Structure
```
jobready-ai/
│
├── app.py                  # Main Streamlit UI
├── requirements.txt
├── README.md
│
└── modules/
    ├── ai_client.py        # Connects to Groq LLM
    ├── resume_handler.py   # Extracts + parses resume with AI
    ├── job_search.py       # Job suggestions + salary ranges + board links
    ├── job_analyzer.py     # Scrapes job URLs + scores match
    ├── cover_letter.py     # Generates tailored cover letters
    ├── interview_prep.py   # Predicts 20 interview questions
    ├── ats_optimizer.py    # ATS keyword analysis + optimization
    └── airtable_logger.py  # Logs applications to Airtable
```

---

## Built By

Chahal Tilak — Self-taught AI developer building practical AI tools.

[GitHub](https://github.com/PurpleC23) • [LinkedIn](https://linkedin.com/in/chahal-tilak-a248a9271)