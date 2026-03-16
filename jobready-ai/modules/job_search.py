import requests
from bs4 import BeautifulSoup
from modules.ai_client import ask_mistral

def search_jobs(skills_text: str, country: str = "Global") -> str:
    """Generate job search suggestions based on resume skills."""
    
    prompt = f"""
    Based on these skills and experience, suggest 8 specific job titles for this candidate.
    
    Format your response as a numbered list like this:
    1. Job Title - Why it fits - Global Remote Salary (USD/month) - {country} Salary - Where to search
    2. Job Title - Why it fits - Global Remote Salary (USD/month) - {country} Salary - Where to search
    
    Include realistic remote salary ranges for both global market in USD and {country} local market.
    
    SKILLS AND EXPERIENCE:
    {skills_text}
    """
    
    result = ask_mistral(prompt)
    return result


def scrape_job_listings(job_title: str) -> dict:
    """Generate direct search URLs for job boards."""
    
    job_encoded = job_title.replace(" ", "+")
    job_hyphen = job_title.replace(" ", "-").lower()
    
    boards = {
        # General
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={job_encoded}&f_WT=2",
        "Indeed": f"https://www.indeed.com/jobs?q={job_encoded}&l=remote",
        "Glassdoor": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={job_encoded}&remoteWorkType=1",
        
        # Remote Specific
        "RemoteOK": f"https://remoteok.com/remote-{job_hyphen}-jobs",
        "Wellfound": f"https://wellfound.com/jobs?q={job_encoded}",
        "WeWorkRemotely": f"https://weworkremotely.com/remote-jobs/search?term={job_encoded}",
        "Remote.co": f"https://remote.co/remote-jobs/search/?search_keywords={job_encoded}",
        "Himalayas": f"https://himalayas.app/jobs?q={job_encoded}",
        
        # Community
        "Reddit r/forhire": f"https://www.reddit.com/r/forhire/search/?q={job_encoded}&sort=new",
        "Reddit r/remotework": f"https://www.reddit.com/r/remotework/search/?q={job_encoded}&sort=new",
        "Reddit r/WorkOnline": f"https://www.reddit.com/r/WorkOnline/search/?q={job_encoded}&sort=new",
        
        # India + Global
        "Naukri": f"https://www.naukri.com/{job_hyphen}-jobs",
        "Internshala": f"https://internshala.com/jobs/{job_hyphen}",
    }
        
    return boards