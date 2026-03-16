import requests
import json
from datetime import datetime

N8N_WEBHOOK_URL = "http://localhost:5678/webhook/cff899ab-ec69-4f1c-ab56-36224890feb1"  # we'll fill this soon

def log_to_n8n(question, answer, sources):
    payload = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
    }
    try:
        r = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
        print(f"✅ Logged to n8n: {r.status_code}")
    except Exception as e:
        print(f"Logging failed: {e}")