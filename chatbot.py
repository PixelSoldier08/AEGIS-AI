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
    .block-container { padding-top: 180px !important; }

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

    /* 3D Spider Projection Zone (Bottom Right) */
    .projection-orb {
        position: fixed; bottom: 50px; right: 50px; z-index: 1000;
        background: radial-gradient(circle, rgba(0,212,255,0.15) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. COGNITIVE ENGINE & VOICE CORE ---
def get_aegis_intel(prompt):
    """Hybrid Intel: Tavily Search + Llama 3.3"""
    try:
        # Step 1: Real-time Data Scan
        scan_data = tavily.search(query=prompt, search_depth="advanced")
        context = scan_data['results']
        
        # Step 2: Processing using Llama 3.3
        chat = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": f"You are AEGIS, a J.A.R.V.I.S.-style AI for Ikki. Location: Tiruchirappalli. "
                               f"Use context: {context}. Be Stark-Industries professional, technical, and concise."
                },
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Neural Error: {str(e)}"

def speak_response(text):
    """Voice Synthesis: Optimized Pitch and Rate for J.A.R.V.I.S."""
    # Escape single quotes and newlines for safe JS transfer
    clean_text = text.replace("'", "\\'").replace("\n", " ")
    st.components.v1.html(f"""
        <script>
        var synth = window.speechSynthesis;
        var utterance = new SpeechSynthesisUtterance('{clean_text}');
        utterance.pitch = 0.85; // Optimized Stark-tech pitch
        utterance.rate = 1.1; // Fast-paced professional rate
        synth.speak(utterance);
        </script>
    """, height=0)

# --- 4. INTERFACE RENDER ---
def render_hud():
    # HUD Core Logic: 502px circumference
    cpu_load = psutil.cpu_percent()
    integrity = int(100 - cpu_load)
    offset = 502 - (integrity / 100) * 502

    st.markdown(f'''
    <div class="aegis-header">
        <div style="position: relative; width: 120px; height: 120px;">
            <svg width="120" height="120" viewBox="0 0 220 220">
                <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
                <circle class="ring" stroke="#00d4ff" stroke-width="14" stroke-dasharray="502" 
                        stroke-dashoffset="{offset}" stroke-linecap="round" fill="transparent" r="80" cx="110" cy="110"
                        style="filter: drop-shadow(0 0 10px #00d4ff);"/>
            </svg>
            <div style="position: absolute; top: 42px; width: 100%; text-align: center;">
                <div style="font-size: 1.3rem; font-weight: bold;">{integrity}%</div>
                <div style="font-size: 0.4rem; letter-spacing: 1px;">INTEGRITY</div>
            </div>
        </div>
        <div class="aegis-data">
            <p class="title">AEGIS // MARK I CORE</p>
            <p class="sub-text">USER: IKKI | LOC: TIRUCHIRAPPALLI | STATUS: ACTIVE</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 3D Spider-Logo Projection (Bottom Right)
    # REPLACE this URL with your RAW link from GitHub for '3dpea.com_download.glb'
    model_url = "https://github.com/PixelSoldier08/AEGIS-AI/raw/refs/heads/main/Spider.glb" 
    
    st.markdown('<div class="projection-orb">', unsafe_allow_html=True)
    st.components.v1.html(f"""
        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
        <model-viewer 
            src="{model_url}" 
            auto-rotate rotation-speed="35deg"
            camera-controls 
            disable-zoom
            style="width: 280px; height: 280px; background: transparent; --progress-bar-color: #00d4ff;"
            shadow-intensity="1">
        </model-viewer>
    """, height=280)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. EXECUTION LOOP ---
render_hud()

if "history" not in st.session_state: 
    st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]): 
        st.markdown(m["content"])

# User Input Core
if cmd := st.chat_input("Command AEGIS..."):
    st.session_state.history.append({"role": "user", "content": cmd})
    with st.chat_message("user"): 
        st.markdown(cmd)

    with st.chat_message("assistant"):
        with st.spinner("SYNAPSING..."):
            ans = get_aegis_intel(cmd)
            st.markdown(ans)
            speak_response(ans) # Trigger voice synthesis
            st.session_state.history.append({"role": "assistant", "content": ans})

# Auto-refresh for animated gauge
time.sleep(2)
st.rerun()
