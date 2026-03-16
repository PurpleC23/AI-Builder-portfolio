from modules.ai_client import ask_mistral

def optimize_for_role(resume_text: str, job_title: str) -> str:
    """Generic ATS optimization for a job title."""
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) optimization specialist.
    
    Analyze this resume against the job title "{job_title}" and provide:
    
    ATS SCORE: (X/100)
    
    KEYWORDS YOU HAVE:
    - (list keywords from resume that match this role)
    
    MISSING KEYWORDS:
    - (list important keywords for {job_title} that are missing from resume)
    
    OPTIMIZED SUMMARY:
    (Rewrite the resume summary/objective in 3-4 sentences using the right ATS keywords for {job_title})
    
    TOP TIPS:
    - (3 specific tips to improve ATS score for this role)
    
    RESUME:
    {resume_text[:2000]}
    """
    
    return ask_mistral(prompt)


def optimize_for_job(resume_text: str, job_text: str) -> str:
    """Specific ATS optimization for a particular job description."""
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) optimization specialist.
    
    Analyze this resume against the specific job description and provide:
    
    ATS SCORE: (X/100)
    
    KEYWORDS YOU HAVE:
    - (list exact keywords from job description that appear in resume)
    
    MISSING KEYWORDS:
    - (list exact keywords from job description missing from resume)
    
    KEYWORD DENSITY ISSUES:
    - (list any keywords that should appear more frequently)
    
    OPTIMIZED SUMMARY:
    (Rewrite the resume summary in 3-4 sentences using exact keywords from the job description)
    
    OPTIMIZED SKILLS SECTION:
    (Rewrite the skills section to match job description keywords exactly)
    
    TOP TIPS:
    - (3 specific tips to improve ATS score for this specific job)
    
    RESUME:
    {resume_text[:2000]}
    
    JOB DESCRIPTION:
    {job_text[:2000]}
    """
    
    return ask_mistral(prompt)