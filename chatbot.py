import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
import openai
import tools 

# --- HUD & STYLE ---
st.set_page_config(page_title="AEGIS: FRIDAY PROTOCOL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #060b14; }
    .stMarkdown, p, h1, h2, h3, li { 
        color: #00f2ff !important; 
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.7);
        font-family: 'Courier New', monospace;
    }
    [data-testid="stChatMessage"] {
        background: rgba(0, 242, 255, 0.05) !important;
        border: 1px solid rgba(0, 242, 255, 0.2) !important;
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CLIENTS ---
def get_clients():
    try:
        g = Groq(api_key=st.secrets["GROQ_API_KEY"])
        o = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) if "OPENAI_API_KEY" in st.secrets else None
        return g, o
    except: return None, None

client, openai_client = get_clients()

# --- VOICE PROTOCOL ---
def speak(text):
    clean = text.replace("'", "").replace('"', "").replace("\n", " ").replace("*", "")
    st.components.v1.html(f"""
        <script>
        window.speechSynthesis.cancel(); 
        setTimeout(() => {{
            var msg = new SpeechSynthesisUtterance('{clean}');
            var voices = window.speechSynthesis.getVoices();
            var female = voices.find(v => v.name.includes('Female') || v.name.includes('Hazel'));
            if (female) msg.voice = female;
            msg.rate = 1.05; msg.pitch = 1.2;
            window.speechSynthesis.speak(msg);
        }}, 100);
        </script>
    """, height=0)

# --- INITIALIZE STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "booted" not in st.session_state:
    st.session_state.booted = False

# --- BOOT SEQUENCE ---
if not st.session_state.booted:
    with st.empty():
        res = requests.get("https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json")
        lottie_json = res.json() if res.status_code == 200 else None
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if lottie_json: st_lottie(lottie_json, height=300)
            bar = st.progress(0)
            for s, v in [("LOADING AEGIS 2.0...", 40), ("SYNCING CORES...", 80), ("FRIDAY ONLINE.", 100)]:
                st.write(f"`{s}`"); bar.progress(v); time.sleep(0.4)
            speak("Welcome back, Boss. All systems green.")
    st.session_state.booted = True

# --- MAIN INTERFACE ---
st.title("AEGIS: FRIDAY PROTOCOL")
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["type"] == "text": st.markdown(m["content"])
        else: st.image(m["content"])

if prompt := st.chat_input("Command FRIDAY..."):
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            # 1. Check for Image Requests
            if any(k in prompt.lower() for k in ["draw", "visualize", "image"]):
                if openai_client:
                    try:
                        res = openai_client.images.generate(model="dall-e-3", prompt=prompt)
                        url = res.data[0].url
                        st.image(url)
                        st.session_state.messages.append({"role": "assistant", "type": "image", "content": url})
                    except: st.error("Graphic link failed.")
                else: st.warning("Visualizer offline.")
            
            # 2. General Conversation with Memory
            else:
                search_context = tools.web_search(prompt)
                history = [{"role": "system", "content": f"You are FRIDAY. Be witty and call the user Boss. Context: {search_context}"}]
                for m in st.session_state.messages:
                    if m["type"] == "text": history.append({"role": m["role"], "content": m["content"]})
                
                ans = client.chat.completions.create(model="llama-3.1-8b-instant", messages=history).choices[0].message.content
                st.markdown(ans); speak(ans)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": ans})
