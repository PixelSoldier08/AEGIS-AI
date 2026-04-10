import streamlit as st
from groq import Groq
import tools

# --- SETUP ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing GROQ_API_KEY in Secrets.")
    st.stop()

st.set_page_config(page_title="AEGIS GLOBAL", page_icon="💠", layout="wide")

# Persistent Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- STARK INDUSTRIES UI ---
st.markdown("""
    <style>
    .stApp { background: #050a10; color: #00d4ff; }
    .stChatMessage { border: 1px solid #1e3a5f; border-radius: 15px; background: #0a192f; }
    </style>
    """, unsafe_allow_html=True)

st.title("💠 AEGIS GLOBAL : CORE")
st.sidebar.title("🎛️ SYSTEM STATUS")
st.sidebar.success("✅ Neural Link: Stable")
st.sidebar.info("Model: Llama-3.1-8b-instant")

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- INTERACTION LOOP ---
if prompt := st.chat_input("Input command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. TOOL ROUTING
        context = ""
        # Search Trigger
        if any(word in prompt.lower() for word in ["news", "today", "update", "latest", "who is"]):
            with st.status("📡 Accessing Global Satellite Network..."):
                context = tools.web_search(prompt)
        
        # Physics Trigger
        if "orbit" in prompt.lower():
            val = "".join(filter(str.isdigit, prompt))
            if val: context = tools.calculate_orbital_mechanics(val)

        # 2. BRAIN EXECUTION
        full_prompt = f"Context: {context}\n\nUser: {prompt}" if context else prompt
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are AEGIS, a high-tech assistant for Ikki. Be concise, scientific, and witty."}] + 
                     st.session_state.messages[:-1] + [{"role": "user", "content": full_prompt}]
        )
        reply = completion.choices[0].message.content
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # 3. BROWSER VOICE
        js = f"""<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance("{reply.replace('"', '').replace("'", "")}"));</script>"""
        st.components.v1.html(js, height=0)
