import streamlit as st
from speech.listen import listen
from speech.speak import speak, stop
from agent import run_agent
from PIL import Image
import os

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")

# Custom Styling
st.markdown("""
    <style>
    .message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 8px;
    }
    .user {
        background-color: #d6f5d6;
        text-align: right;
    }
    .assistant {
        background-color: #ffe6f0;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# Session state init
if "chat" not in st.session_state:
    st.session_state.chat = []

# ALSO maintain history for Gemini
if "history" not in st.session_state:
    st.session_state.history = []

if "assistant_name" not in st.session_state:
    st.session_state.assistant_name = "Sam"

# Sidebar assistant selection
st.sidebar.title("🧠 Choose Assistant")
selected = st.sidebar.radio("Assistant Avatar", ["Sam", "Andy", "Harvey"], index=["Sam", "Andy", "Harvey"].index(st.session_state.assistant_name))
st.session_state.assistant_name = selected
avatar_path = f"assets/{selected.lower()}.png"

# Sidebar avatar preview
st.sidebar.image(avatar_path, width=120, caption=f"{selected} (AI)")

# Stop and reset
col1, col2 = st.sidebar.columns(2)
if col1.button("⏹️ Stop"):
    stop()
if col2.button("🔄 Reset"):
    st.session_state.chat = []
    st.session_state.history = []
    st.rerun()

st.title(f"🤖 {selected} - Your Personal AI Assistant")

# Display chat
for role, msg in st.session_state.chat:
    class_name = "assistant" if role == "assistant" else "user"
    st.markdown(f'<div class="message {class_name}">{msg}</div>', unsafe_allow_html=True)

# Input form
with st.form("chat_input", clear_on_submit=True):
    user_input = st.text_input("Your message", placeholder="Type and press Enter")
    submit = st.form_submit_button("Send")

if submit and user_input.strip():
    st.session_state.chat.append(("user", user_input))
    st.session_state.history.append(("user", user_input))
    with st.spinner("Thinking..."):
        response = run_agent(user_input)
    st.session_state.chat.append(("assistant", response))
    st.session_state.history.append(("bot", response))
    speak(response)
    st.rerun()

# Voice input
st.markdown("---")
if st.button("🎤 Use Voice Instead"):
    with st.spinner("Listening..."):
        voice_text = listen()
    st.session_state.chat.append(("user", voice_text))
    st.session_state.history.append(("user", voice_text))
    with st.spinner("Thinking..."):
        response = run_agent(voice_text)
    st.session_state.chat.append(("assistant", response))
    st.session_state.history.append(("bot", response))
    speak(response)
    st.rerun()
