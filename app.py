import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

XAI_API_KEY = os.getenv("XAI_API_KEY")

def ask_grok(user_message):
    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2-latest",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

st.set_page_config(page_title="Grok Chatbot", layout="centered")
st.title("🤖 Grok AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        reply = ask_grok(user_input)
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

