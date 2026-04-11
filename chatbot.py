import streamlit as st
import psutil
import time
import requests # For Weather
from groq import Groq # or your preferred provider

# --- CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# (Keep your CSS Block here - the one we refined for the floating HUD)

# --- THE BRAIN (API CONNECTION) ---
# Ensure you have 'GROQ_API_KEY' set in your GitHub Secrets or Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_aegis_response(user_input):
    """This connects the UI to the actual AI model"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are AEGIS, a highly advanced AI developed for Ikki. You have a Stark-Industries personality. Be helpful, concise, and technical."
                },
                {"role": "user", "content": user_input}
            ],
            model="llama3-70b-8192", # High-speed model for the HUD vibe
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Neural Link Error: {str(e)}"

# --- RENDER HUD ---
# (Insert the render_aegis_hud() function we built previously here)

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # This is where the magic happens - he actually 'thinks' now
        with st.spinner("ANALYZING..."):
            response = get_aegis_response(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- REFRESH ---
time.sleep(2)
st.rerun()
