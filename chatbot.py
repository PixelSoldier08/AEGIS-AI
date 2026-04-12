import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
from tavily import TavilyClient

# --- 1. HUD STYLING ---
st.set_page_config(page_title="AEGIS OS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #060b14; color: #00f2ff; }
    .stMarkdown, p, h1, h2, h3 { 
        color: #00f2ff !important; 
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.7);
        font-family: 'Courier New', monospace;
    }
    [data-testid="stChatMessage"] {
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. API INITIALIZATION ---
def get_globals():
    try:
        g_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        t_client = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        return g_client, t_client
    except Exception as e:
        st.error(f"Configuration Error: Check your Streamlit Secrets! ({e})")
        return None, None

client, tavily = get_globals()

# --- 3. UTILITIES ---
def load_lottie(url):
    try:
        res = requests.get(url, timeout=5)
        return res.json() if res.status_code == 200 else None
    except: return None

def speak(text):
    clean = text.replace("'", "").replace("\n", " ")
    st.components.v1.html(f"<script>var m=new SpeechSynthesisUtterance('{clean}');m.rate=1.0;m.pitch=0.8;window.speechSynthesis.speak(m);</script>", height=0)

# --- 4. BOOT ANIMATION ---
if 'booted' not in st.session_state:
    intro = st.empty()
    with intro.container():
        lottie_json = load_lottie("https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if lottie_json: st_lottie(lottie_json, height=400, key="boot")
            bar = st.progress(0)
            msg = st.empty()
            for i, s in enumerate(["LOADING AEGIS...", "SYNCING...", "ONLINE."]):
                msg.markdown(f"`{s}`")
                bar.progress((i + 1) * 33)
                time.sleep(0.7)
            speak("Welcome home, sir.")
    st.session_state.booted = True
    intro.empty()

# --- 5. CHAT LOGIC ---
if st.session_state.get('booted') and client:
    st.title("AEGIS v2.0")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Command AEGIS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                # A. Fail-safe Search
                context = "No live data found."
                try:
                    search = tavily.search(query=prompt)
                    context = str(search['results'])
                except: pass

                # B. Fail-safe Reasoning
                try:
                    response = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[
                            {"role": "system", "content": f"You are AEGIS. Use this info: {context}"},
                            {"role": "user", "content": prompt}
                        ]
                    ).choices[0].message.content
                except Exception as e:
                    response = f"Sir, my neural link is unstable. (Error: {e})"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
