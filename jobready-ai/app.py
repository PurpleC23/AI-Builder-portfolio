import streamlit as st
from modules.resume_handler import extract_resume_text, parse_resume_with_ai
from modules.job_search import search_jobs, scrape_job_listings
from modules.job_analyzer import scrape_job, analyze_match
from modules.cover_letter import generate_cover_letter
from modules.interview_prep import generate_interview_questions
from modules.airtable_logger import log_job_to_airtable
from modules.job_analyzer import scrape_job, analyze_match, extract_job_details
from modules.ats_optimizer import optimize_for_role, optimize_for_job


# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Job Ready",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 0 20px;
        border-radius: 6px 6px 0 0;
        border: 1px solid #3a1a1a;
        border-bottom: none;
        background-color: #1a1010;
        color: #888;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(139, 30, 30, 0.75) !important;
        color: white !important;
        border-color: rgba(139, 30, 30, 0.75) !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(139, 30, 30, 0.4);
        color: white;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: rgba(139, 30, 30, 0.15) !important;
        border-right: 1px solid rgba(139, 30, 30, 0.4);
    }
            
        # Mobile optimisation
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            padding: 0 10px;
            font-size: 12px;
            height: 36px;
        }
        .stButton button {
            width: 100%;
        }
        .stDownloadButton button {
            width: 100%;
        }
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State (memory between tabs) ───────────────────────────────────────
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "parsed_resume" not in st.session_state:
    st.session_state.parsed_resume = ""
if "job_text" not in st.session_state:
    st.session_state.job_text = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = "Your Name"
if "job_suggestions" not in st.session_state:
    st.session_state.job_suggestions = ""

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("JobReady")
    st.caption("Your personal job hunting assistant")
    st.divider()
    
    if st.session_state.resume_text:
        st.success("Resume loaded")
    else:
        st.warning("No resume uploaded yet")
    
    if st.session_state.job_text:
        st.success("Job loaded")
    else:
        st.info("No job analyzed yet")
    
    st.divider()
    st.caption("Powered by Groq — fast free AI")

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Resume",
    "Job Search", 
    "Job Analyzer",
    "Cover Letter",
    "Interview Prep",
    "ATS Optimizer"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RESUME
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("📄 Upload Your Resume")
    st.caption("Upload once — all other features use this automatically.")
    
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    st.session_state.user_name = st.text_input("Your Full Name:", placeholder="e.g. Sam Winchester")
    if uploaded_file:
        with st.spinner("Reading your resume..."):
            raw_text = extract_resume_text(uploaded_file)
            st.session_state.resume_text = raw_text
        
        st.success("Resume uploaded successfully!")
        
        if st.button("Click to Extract", type="primary"):
            with st.spinner("Your Resume is being analysed..."):
                parsed = parse_resume_with_ai(raw_text)
                st.session_state.parsed_resume = parsed["parsed"]
            
            st.subheader("Key Points:")
            st.markdown(st.session_state.parsed_resume)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — JOB SEARCH
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("🔍︎ Job Search")
    st.caption("Based on your resume, find jobs that match your profile.")
    
    if not st.session_state.resume_text:
        st.warning("Please upload your resume in the Resume tab first.")
    else:
        # Country selector
        country_option = st.selectbox(
            "Select market for salary ranges:",
            ["Global (USD)", "India (INR)", "Custom"]
        )
        
        if country_option == "Custom":
            country = st.text_input("Enter your country:", placeholder="e.g. Germany, Canada, UK")
        elif country_option == "India (INR)":
            country = "India (INR)"
        else:
            country = "Global (USD)"
        
        if st.button("Find Matching Jobs", type="primary"):
            with st.spinner("Finding the best jobs for you..."):
                suggestions = search_jobs(
                    st.session_state.parsed_resume or st.session_state.resume_text,
                    country
                )
                st.session_state.job_suggestions = suggestions
            
            st.subheader("Recommended Jobs:")
            st.markdown(suggestions)
        
        st.divider()
        st.subheader("Search on Job Boards")
        
        # Job title input with suggestions
        if "job_suggestions" in st.session_state and st.session_state.job_suggestions:
            # Extract job titles from suggestions
            lines = st.session_state.job_suggestions.split("\n")
            suggested_titles = []
            for line in lines:
                if line.strip() and line.strip()[0].isdigit():
                    title = line.split("-")[0].strip()
                    title = line.lstrip("0123456789. ").replace("**", "").replace("*", "").strip()
                    title = title.split(" - ")[0].strip()
                    if title:
                        suggested_titles.append(title)
            
            if suggested_titles:
                suggested_titles.append("Type my own...")
                selected = st.selectbox("Choose a job title:", suggested_titles)
                
                if selected == "Type my own...":
                    job_title_input = st.text_input("Enter job title:", placeholder="e.g. AI Developer")
                else:
                    job_title_input = selected
            else:
                job_title_input = st.text_input("Enter a job title:", placeholder="e.g. AI Developer")
        else:
            job_title_input = st.text_input("Enter a job title:", placeholder="e.g. AI Developer")
        
        if job_title_input and job_title_input != "Type my own...":
            links = scrape_job_listings(job_title_input)
            
            st.write("**General:**")
            cols = st.columns(3)
            general = ["LinkedIn", "Indeed", "Glassdoor"]
            for i, name in enumerate(general):
                with cols[i]:
                    st.link_button(name, links[name])
            
            st.write("**Remote:**")
            cols = st.columns(4)
            remote = ["RemoteOK", "Wellfound", "WeWorkRemotely", "Remote.co"]
            for i, name in enumerate(remote):
                with cols[i]:
                    st.link_button(name, links[name])
            
            st.write("**Community:**")
            cols = st.columns(3)
            community = ["Reddit r/forhire", "Reddit r/remotework", "Reddit r/WorkOnline"]
            for i, name in enumerate(community):
                with cols[i]:
                    st.link_button(name, links[name])
            
            st.write("**India:**")
            cols = st.columns(2)
            india = ["Naukri", "Internshala"]
            for i, name in enumerate(india):
                with cols[i]:
                    st.link_button(name, links[name])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — JOB ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("📈 Job Analyzer")
    st.caption("Paste any job URL — we scrape it and score your match.")
    
    if not st.session_state.resume_text:
        st.warning("Please upload your resume in the Resume tab first.")
    else:
        job_url = st.text_input("Paste job posting URL:", placeholder="https://...")
        
        if job_url:
            if st.button("⚡ Analyze This Job", type="primary"):
                with st.spinner("Scraping job posting..."):
                    job_text = scrape_job(job_url)
                    st.session_state.job_text = job_text
                
                with st.spinner("Rating..."):
                    analysis = analyze_match(
                        st.session_state.resume_text,
                        st.session_state.job_text
                    )
                
                st.subheader("Match Analysis:")
                st.markdown(analysis)
                # Extract match score from analysis
                score = ""
                for line in analysis.split("\n"):
                    if "MATCH SCORE" in line:
                        digits = ''.join(filter(str.isdigit, line))
                        score = digits[:2] if len(digits) > 2 else digits
                        break

                # Log to Airtable
                details = extract_job_details(st.session_state.job_text)

                logged = log_job_to_airtable(
                    job_title=details["job_title"],
                    company=details["company"],
                    job_url=job_url,
                    match_score=score,
                    notes=analysis
                )

                if logged:
                    st.success("✅ Job logged to Airtable!")
                else:
                    st.warning("⚠️ Airtable logging failed — check your token.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — COVER LETTER
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.header("✉︎ Cover Letter Generator")
    st.caption("Tailored to the specific job — not a generic template.")
    
    if not st.session_state.resume_text:
        st.warning("Please upload your resume in the Resume tab first.")
    elif not st.session_state.job_text:
        st.warning("Please analyze a job in the Job Analyzer tab first.")
    else:
        extra_info = st.text_area(
            "Any extra context to include? (optional)",
            placeholder="e.g. I've used their product for 2 years, mention my freelance experience..."
        )
        
        if st.button("✉︎ Generate Cover Letter", type="primary"):
            with st.spinner("Writing your cover letter..."):
                letter = generate_cover_letter(
                    st.session_state.resume_text,
                    st.session_state.job_text,
                    extra_info
                )
            if "Regards" in letter:
                 letter = letter.split("Regards")[0] + f"Regards,\n\n{st.session_state.user_name}"
            
            # Update Airtable with cover letter
            if st.session_state.job_text:
                log_job_to_airtable(
                    job_title="Cover Letter Generated",
                    company="See Notes",
                    job_url="N/A",
                    match_score="0",
                    cover_letter=letter,
                    notes="Cover letter generated"
                )

            st.subheader("Your Cover Letter:")
            st.markdown(letter)
            from fpdf import FPDF

            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=25)
            pdf.set_font("Courier", size=10)

            page_width = pdf.w - 20
            for line in letter.split("\n"):
                if line.strip() == "":
                    pdf.ln(4)
                else:
                    safe_line = line.strip().encode("latin-1", errors="replace").decode("latin-1")
                    pdf.multi_cell(page_width, 6, safe_line)
            
            pdf.ln(10)
            pdf_bytes = bytes(pdf.output())

            st.download_button(
                "⬇️ Download as PDF",
                data=pdf_bytes,
                file_name="cover_letter.pdf",
                mime="application/pdf"
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — INTERVIEW PREP
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.header("🗣️ Interview Prep")
    st.caption("Predicted questions with tailored answer frameworks.")
    
    if not st.session_state.resume_text:
        st.warning("Please upload your resume in the Resume tab first.")
    elif not st.session_state.job_text:
        st.warning("Please analyze a job in the Job Analyzer tab first.")
    else:
        if st.button("🗣️ Generate Interview Questions", type="primary"):
            with st.spinner("Predicting your interview questions..."):
                questions = generate_interview_questions(
                    st.session_state.resume_text,
                    st.session_state.job_text
                )
            
            st.subheader("Your Interview Prep Guide:")
            st.markdown(questions)
            st.download_button(
                "⬇️ Download as TXT",
                questions,
                file_name="interview_prep.txt",
                mime="text/plain"
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — ATS OPTIMIZER
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.header("📋 ATS Optimizer")
    st.caption("Optimize your resume to pass Applicant Tracking Systems.")
    
    if not st.session_state.resume_text:
        st.warning("Please upload your resume in the Resume tab first.")
    else:
        mode = st.radio(
            "Choose optimization mode:",
            ["Generic — by job title", "Specific — by job description"]
        )
        
        if mode == "Generic — by job title":
            job_title = st.text_input(
                "Enter job title to optimize for:",
                placeholder="e.g. AI Developer, LangChain Engineer"
            )
            
            if job_title:
                if st.button("Optimize for this Role", type="primary"):
                    with st.spinner("Analyzing your resume against ATS requirements..."):
                        result = optimize_for_role(
                            st.session_state.resume_text,
                            job_title
                        )
                    
                    st.subheader("ATS Analysis:")
                    st.markdown(result)
                    st.download_button(
                        "Download ATS Report",
                        result,
                        file_name="ats_report.txt",
                        mime="text/plain"
                    )
        
        else:
            if not st.session_state.job_text:
                st.warning("Please analyze a job in the Job Analyzer tab first.")
            else:
                st.success("Using job description from Job Analyzer tab.")
                
                if st.button("Optimize for this Job", type="primary"):
                    with st.spinner("Analyzing your resume against this specific job..."):
                        result = optimize_for_job(
                            st.session_state.resume_text,
                            st.session_state.job_text
                        )
                    
                    st.subheader("ATS Analysis:")
                    st.markdown(result)
                    st.download_button(
                        "Download ATS Report",
                        result,
                        file_name="ats_report.txt",
                        mime="text/plain"
                    )