import streamlit as st
import psutil
import time
from groq import Groq
from tavily import TavilyClient

# --- 1. CORE SYSTEM CONFIGURATION ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# Initialize Neural and Search Links
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except Exception as e:
    st.error(f"SYSTEM FAILURE: Check Secrets. Error: {e}")

# --- 2. HOLOGRAPHIC HUD (STARK DESIGN CORE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* Stark Mode Theme */
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container { padding-top: 150px !important; }

    /* The Pulsing HUD (Top Left Orb) */
    .aegis-header {
        position: fixed; top: 25px; left: 40px; z-index: 9999;
        display: flex; align-items: center; gap: 30px; pointer-events: none;
    }
    .aegis-data { border-left: 3px solid #00d4ff; padding-left: 20px; }
    .title { font-size: 1.6rem; font-weight: bold; text-shadow: 0 0 15px #00d4ff; margin: 0; }
    .sub-text { font-size: 0.75rem; letter-spacing: 2px; opacity: 0.8; margin-top: 5px; }
    
    /* HUD Circle Animation */
    .ring { transition: stroke-dashoffset 1s ease; transform: rotate(-90deg); transform-origin: center; }

    /* Fixed 3D Projection at Bottom Right */
    .projection-zone {
        position: fixed; bottom: 30px; right: 30px; z-index: 9999;
        width: 280px; height: 280px;
        background: radial-gradient(circle, rgba(0,212,255,0.15) 0%, rgba(0,0,0,0) 70%);
        pointer-events: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SPEECH & INTEL ENGINES ---
def speak(text):
    """Refined Voice Core: Stark Industries Pitch"""
    if text:
        clean_text = text.replace("'", "\\'").replace("\n", " ")
        st.components.v1.html(f"""
            <script>
            window.speechSynthesis.cancel(); 
            var u = new SpeechSynthesisUtterance('{clean_text}');
            u.pitch = 0.85; u.rate = 1.05; u.volume = 1.0;
            window.speechSynthesis.speak(u);
            </script>
        """, height=0)

def get_aegis_intel(prompt):
    """Hybrid Intel: Tavily Search + Llama 3.3"""
    try:
        search = tavily.search(query=prompt, search_depth="advanced")
        context = search['results']
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are AEGIS, a J.A.R.V.I.S.-style AI for Ikki. Tiruchirappalli context: {context}. Be professional and technical."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile" # Updated to supported model
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Neural Error: {str(e)}"

# --- 4. INTERFACE RENDER ---
def render_interface():
    # HUD Core Logic
    cpu_load = psutil.cpu_percent()
    integrity = int(100 - cpu_load)
    offset = 502 - (integrity / 100) * 502

    st.markdown(f'''
    <div class="aegis-header">
        <div style="position: relative; width: 110px; height: 110px;">
            <svg width="110" height="110" viewBox="0 0 220 220">
                <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
                <circle class="ring" stroke="#00d4ff" stroke-width="14" stroke-dasharray="502" 
                        stroke-dashoffset="{offset}" stroke-linecap="round" fill="transparent" r="80" cx="110" cy="110"
                        style="filter: drop-shadow(0 0 10px #00d4ff);"/>
            </svg>
            <div style="position: absolute; top: 38px; width: 100%; text-align: center;">
                <div style="font-size: 1.2rem; font-weight: bold;">{integrity}%</div>
                <div style="font-size: 0.4rem; letter-spacing: 1px;">INTEGRITY</div>
            </div>
        </div>
        <div class="aegis-data">
            <p class="title">AEGIS // MARK I CORE</p>
            <p class="sub-text">USER: IKKI | LOC: TIRUCHIRAPPALLI | STATUS: ACTIVE</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 3D Spider Projection - Locked to Bottom Right
    model_url = "https://github.com/PixelSoldier08/AEGIS-AI/blob/main/Spider.glb?raw=true"
    
    st.markdown(f'''
    <div class="projection-zone">
        <iframe srcdoc='
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <body style="margin: 0; background: transparent; overflow: hidden;">
                <model-viewer src="{model_url}" auto-rotate rotation-speed="40deg" 
                    camera-controls disable-zoom style="width: 280px; height: 280px; background: transparent; outline: none;">
                </model-viewer>
            </body>
        ' style="width: 280px; height: 280px; border: none; background: transparent;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 5. CHAT ENGINE ---
render_interface()

if "history" not in st.session_state:
    st.session_state.history = []
if "last_response" not in st.session_state:
    st.session_state.last_response = None

# Display History
for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# User Input
if cmd := st.chat_input("Command AEGIS..."):
    st.session_state.history.append({"role": "user", "content": cmd})
    with st.chat_message("user"):
        st.markdown(cmd)
    
    with st.chat_message("assistant"):
        with st.spinner("SYNAPSING..."):
            ans = get_aegis_intel(cmd)
            st.markdown(ans)
            st.session_state.history.append({"role": "assistant", "content": ans})
            st.session_state.last_response = ans
            st.rerun()

# Trigger Voice
if st.session_state.last_response:
    speak(st.session_state.last_response)
    st.session_state.last_response = None

# Passive HUD Update
time.sleep(3)
st.rerun()
