from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

try:
    import streamlit as st
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
except:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def ask_mistral(prompt: str, system: str = "") -> str:
    """Send a prompt to Groq and get a response."""
    
    messages = []
    
    if system:
        messages.append({"role": "system", "content": system})
    
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=4000
    )
    
    return response.choices[0].message.content