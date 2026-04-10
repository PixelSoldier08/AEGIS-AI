import streamlit as st
from groq import Groq
import tools

# --- 1. SECURE CONNECTION ---
try:
    # This looks for the key you pasted in Streamlit Advanced Settings
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Key missing or invalid. Check your Streamlit Secrets.")
    st.stop()

st.set_page_config(page_title="AEGIS GLOBAL", page_icon="💠")

# Initialize memory if it's the first time loading
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💠 AEGIS GLOBAL : NODE 01")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 2. INPUT HANDLING ---
if prompt := st.chat_input("Command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We add a safety check: Only call Groq if there are messages
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AEGIS, a witty AI assistant."}
                ] + st.session_state.messages,
                model="llama3-8b-8192",
            )
            reply = chat_completion.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # Browser Voice Trigger
            js = f"""<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance("{reply.replace('"', '').replace("'", "")}"));</script>"""
            st.components.v1.html(js, height=0)
            
        except Exception as e:
            st.error(f"AEGIS Core Error: {str(e)}")
