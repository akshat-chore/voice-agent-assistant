import os
import requests
from dotenv import load_dotenv
from tools.calculator import solve_math
from tools.web_search import search_web
import requests

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini(prompt):
    from streamlit import session_state  # needed to access history

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    # 🧠 Include prior Q&A from history
    messages = []
    if "history" in session_state:
        for sender, msg in session_state.history[-8:]:  # limit to last 4 exchanges
            if sender == "user":
                messages.append({"role": "user", "parts": [{"text": msg}]})
            elif sender == "bot":
                messages.append({"role": "model", "parts": [{"text": msg}]})

    # Add latest user message
    messages.append({"role": "user", "parts": [{"text": prompt}]})

    data = {"contents": messages}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        content = response.json()
        return content['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Gemini API error: {e}"



def run_agent(query):
    q = query.lower()
    if any(op in q for op in ['+', '-', '*', '/', 'calculate']):
        return solve_math(query)
    elif "search" in q or "look up" in q:
        return search_web(query)
    else:
        return call_gemini(query)
