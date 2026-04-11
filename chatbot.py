import streamlit as st
import psutil
import time
from groq import Groq
from tavily import TavilyClient

# --- 1. SYSTEM INITIALIZATION ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# Establish Neural and Data Links
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except Exception as e:
    st.error(f"Neural Link Failure: Check API Keys in Secrets. Error: {e}")

# --- 2. HOLOGRAPHIC STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container { padding-top: 180px !important; }

    /* Floating HUD Matrix */
    .aegis-header {
        position: fixed; top: 25px; left: 40px; z-index: 9999;
        display: flex; align-items: center; gap: 30px; pointer-events: none;
    }
    .aegis-data-stream { border-left: 3px solid #00d4ff; padding-left: 20px; }
    .title { font-size: 1.6rem; font-weight: bold; text-shadow: 0 0 15px #00d4ff; margin: 0; }
    .status { font-size: 0.75rem; letter-spacing: 2px; opacity: 0.8; margin-top: 5px; }
    
    /* 3D Projection Zone */
    .projection-zone {
        position: fixed; bottom: 30px; right: 30px; z-index: 1000;
        background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CORE AEGIS INTELLIGENCE ---
def get_aegis_intel(prompt):
    """Hybrid Intelligence: Tavily Search + Llama 3.3 Logic"""
    try:
        # Live Search Data Extraction
        search_result = tavily.search(query=prompt, search_depth="advanced")
        context = search_result['results']
        
        # Neural Processing with Context
        chat = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": f"You are AEGIS, a J.A.R.V.I.S.-style AI for Ikki. Location: Tiruchirappalli. "
                               f"Use this live data context: {context}. Be professional, technical, and concise."
                },
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile" 
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Neural Error: {str(e)}"

def speak(text):
    """Neural Voice Synthesis: Stark Industries Pitch"""
    clean_text = text.replace("'", "\\'")
    st.components.v1.html(f"""
        <script>
        var synth = window.speechSynthesis;
        var u = new SpeechSynthesisUtterance('{clean_text}');
        u.pitch = 0.85; u.rate = 1.1;
        synth.speak(u);
        </script>
    """, height=0)

# --- 4. INTERFACE COMPONENTS ---
def render_ui():
    # HUD Rendering: Core Integrity Circle
    cpu_load = psutil.cpu_percent()
    integrity = int(100 - cpu_load)
    offset = 502 - (integrity / 100) * 502

    st.markdown(f'''
    <div class="aegis-header">
        <div style="position: relative; width: 120px; height: 120px;">
            <svg width="120" height="120" viewBox="0 0 220 220">
                <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
                <circle stroke="#00d4ff" stroke-width="14" stroke-dasharray="502" 
                        stroke-dashoffset="{offset}" stroke-linecap="round" fill="transparent" r="80" cx="110" cy="110"
                        style="transform: rotate(-90deg); transform-origin: center; filter: drop-shadow(0 0 10px #00d4ff); transition: 1s;"/>
            </svg>
            <div style="position: absolute; top: 42px; width: 100%; text-align: center;">
                <div style="font-size: 1.3rem; font-weight: bold;">{integrity}%</div>
                <div style="font-size: 0.4rem; letter-spacing: 1px;">INTEGRITY</div>
            </div>
        </div>
        <div class="aegis-data-stream">
            <p class="title">AEGIS // MARK I CORE</p>
            <p class="status">USER: IKKI | LOC: TIRUCHIRAPPALLI | STATUS: ACTIVE</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 3D Spider-Logo Projection
    # Replace with your Raw GitHub URL
    model_url = "https://github.com/PixelSoldier08/AEGIS-AI/raw/refs/heads/main/download.gltf" 
    
    with st.container():
        st.markdown('<div class="projection-zone">', unsafe_allow_html=True)
        st.components.v1.html(f"""
            <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
            <model-viewer 
                src="{model_url}" 
                auto-rotate rotation-speed="35deg"
                camera-controls 
                disable-zoom
                style="width: 280px; height: 280px; background: transparent;"
                shadow-intensity="1">
            </model-viewer>
        """, height=280)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. EXECUTION ---
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
        with st.spinner("SYNAPSING..."):
            intel = get_aegis_intel(cmd)
            st.markdown(intel)
            speak(intel)
            st.session_state.history.append({"role": "assistant", "content": intel})

# Live HUD Refresh
time.sleep(2)
st.rerun()
