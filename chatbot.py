import streamlit as st
from groq import Groq
import tools # Your laboratory file

# --- INITIALIZATION ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="AEGIS GLOBAL", page_icon="💠", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- STARK UI ---
st.title("💠 AEGIS GLOBAL : NODE 01")
st.caption("Status: Cloud-Linked via Groq | Engine: Llama 3")

# --- THE LOGIC ---
if prompt := st.chat_input("Command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # We send the request to the Cloud Brain (Groq)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are AEGIS. Respond as a witty, helpful AI."}
            ] + st.session_state.messages,
            model="llama3-8b-8192",
        )
        reply = chat_completion.choices[0].message.content
        st.markdown(reply)
        
    st.session_state.messages.append({"role": "assistant", "content": reply})
    
    # Browser Voice Trigger
    js = f"""<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance("{reply.replace('"', '')}"));</script>"""
    st.components.v1.html(js, height=0)