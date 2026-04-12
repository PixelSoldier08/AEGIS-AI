import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
from tavily import TavilyClient

# --- 1. HUD & INTERFACE CONFIG ---
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

# --- 2. BRAIN INITIALIZATION ---
def get_globals():
    try:
        g_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        t_client = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        return g_client, t_client
    except Exception as e:
        st.error(f"Sir, API configuration is missing: {e}")
        return None, None

client, tavily = get_globals()

# --- 3. CORE UTILITIES ---
def load_lottie(url):
    try:
        res = requests.get(url, timeout=5)
        return res.json() if res.status_code == 200 else None
    except: return None

def speak(text):
    clean = text.replace("'", "").replace("\n", " ")
    st.components.v1.html(f"<script>var m=new SpeechSynthesisUtterance('{clean}');m.rate=1.0;m.pitch=0.8;window.speechSynthesis.speak(m);</script>", height=0)

# --- 4. BOOT SEQUENCE ---
if 'booted' not in st.session_state:
    intro = st.empty()
    with intro.container():
        lottie_json = load_lottie("https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if lottie_json: st_lottie(lottie_json, height=400, key="boot")
            bar = st.progress(0)
            msg = st.empty()
            for i, s in enumerate(["UPDATING NEURAL LINKS...", "STABILIZING LLAMA 3.1...", "ONLINE."]):
                msg.markdown(f"`{s}`")
                bar.progress((i + 1) * 33)
                time.sleep(0.7)
            speak("Welcome home, sir. Neural links stabilized.")
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
            with st.spinner("Processing..."):
                # A. Search Engine
                context = ""
                try:
                    search = tavily.search(query=prompt)
                    context = str(search['results'])
                except: context = "No live data available."

                # B. The AI Brain (Updated to supported models)
                # We try Llama 3.1 first, then fallback to Mixtral if it fails
                models_to_try = ["llama-3.1-8b-instant", "llama3-70b-8192", "mixtral-8x7b-32768"]
                response = ""
                
                for model in models_to_try:
                    try:
                        chat_completion = client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": f"You are AEGIS. Use this live data: {context}"},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        response = chat_completion.choices[0].message.content
                        break # Success!
                    except Exception as e:
                        response = f"Sir, neural link failed on {model}. Retrying..."
                        continue
                
                if not response or "Retrying" in response:
                    response = "Sir, all neural links are currently decommissioned by the provider."

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
