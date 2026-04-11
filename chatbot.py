import streamlit as st
import psutil
from groq import Groq
from tavily import TavilyClient

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. HOLOGRAPHIC INTERFACE DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container { padding-top: 150px !important; }

    .aegis-header {
        position: fixed; top: 25px; left: 40px; z-index: 9999;
        display: flex; align-items: center; gap: 20px;
    }
    
    .projection-zone {
        position: fixed; bottom: 30px; right: 30px; z-index: 9999;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SPEECH CORE ---
def speak(text):
    if text:
        clean_text = text.replace("'", "\\'").replace("\n", " ")
        st.components.v1.html(f"""
            <script>
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance('{clean_text}');
            u.pitch = 0.85; u.rate = 1.05; 
            window.speechSynthesis.speak(u);
            </script>
        """, height=0)

# --- 4. HUD & 3D RENDERING ---
def render_ui():
    integrity = int(100 - psutil.cpu_percent())
    offset = 502 - (integrity / 100) * 502
    
    st.markdown(f'''
    <div class="aegis-header">
        <svg width="100" height="100" viewBox="0 0 220 220">
            <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
            <circle stroke="#00d4ff" stroke-width="12" stroke-dasharray="502" 
                    stroke-dashoffset="{offset}" stroke-linecap="round" fill="transparent" r="80" cx="110" cy="110"
                    style="transform: rotate(-90deg); transform-origin: center; filter: drop-shadow(0 0 10px #00d4ff); transition: 1.5s;"/>
        </svg>
        <div style="border-left: 2px solid #00d4ff; padding-left: 20px;">
            <p style="font-size: 1.5rem; font-weight: bold; margin: 0;">AEGIS // MARK I</p>
            <p style="font-size: 0.7rem; opacity: 0.8; margin: 0;">USER: IKKI | STATUS: ACTIVE</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # --- THE ABSOLUTE DIRECT LINK ---
    # Optimized URL path for faster loading from Tiruchirappalli
    model_url = "https://raw.githubusercontent.com/PixelSoldier08/AEGIS-AI/main/download.glb"
    
    st.markdown(f'''
    <div class="projection-zone">
        <iframe srcdoc='
            <html>
            <head>
                <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            </head>
            <body style="margin: 0; background: transparent; overflow: hidden;">
                <model-viewer src="{model_url}" auto-rotate rotation-speed="40deg" 
                    camera-controls disable-zoom 
                    loading="eager"
                    exposure="1.1"
                    shadow-intensity="1"
                    style="width: 320px; height: 320px; background: transparent; outline: none;">
                </model-viewer>
            </body>
            </html>
        ' style="width: 320px; height: 320px; border: none; background: transparent;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 5. CHAT ENGINE ---
render_ui()

if "history" not in st.session_state:
    st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if cmd := st.chat_input("Command AEGIS..."):
    st.session_state.history.append({"role": "user", "content": cmd})
    with st.chat_message("user"):
        st.markdown(cmd)
    
    with st.chat_message("assistant"):
        # Synthesizing Groq Intel for Ikki
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": cmd}],
            model="llama-3.3-70b-versatile"
        )
        ans = chat.choices[0].message.content
        st.markdown(ans)
        st.session_state.history.append({"role": "assistant", "content": ans})
        speak(ans)
        st.rerun()
