import streamlit as st
import psutil
import time
from groq import Groq

# --- 1. CORE SYSTEM INITIALIZATION ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# Establish Neural Link using Llama 3.3
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Neural Link Failure: API Key missing in Secrets.")

# Safety check for 3D Component
try:
    from streamlit_threejs import threejs_component
    THREE_LINK = True
except ImportError:
    THREE_LINK = False

# --- 2. HOLOGRAPHIC DESIGN CORE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container { padding-top: 180px !important; }

    /* Floating Header Matrix */
    .aegis-header {
        position: fixed; top: 25px; left: 40px; z-index: 9999;
        display: flex; align-items: center; gap: 30px; pointer-events: none;
    }
    .aegis-data-stream { border-left: 3px solid #00d4ff; padding-left: 20px; }
    .title { font-size: 1.6rem; font-weight: bold; text-shadow: 0 0 15px #00d4ff; margin: 0; }
    .status { font-size: 0.75rem; letter-spacing: 2px; opacity: 0.8; margin-top: 5px; }
    
    /* Gauge Animation */
    .ring { transition: stroke-dashoffset 1s ease; transform: rotate(-90deg); transform-origin: center; }

    /* 3D Projection Zone */
    .projection-orb {
        position: fixed; bottom: 50px; right: 50px; z-index: 1000;
        background: radial-gradient(circle, rgba(0,212,255,0.15) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SYSTEM FUNCTIONS ---
def get_aegis_intel(prompt):
    """Calculates responses using Llama 3.3 with Physics & Local context"""
    try:
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are AEGIS, a J.A.R.V.I.S.-style AI for Ikki. Location: Tiruchirappalli. You are an expert in Physics, Python, and local Tamil Nadu insights. Be professional, concise, and technical."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Neural Error: {str(e)}"

def speak(text):
    """Voice synthesis with a deep Stark-tech tone"""
    clean_text = text.replace("'", "\\'")
    st.components.v1.html(f"""
        <script>
        var synth = window.speechSynthesis;
        var utterance = new SpeechSynthesisUtterance('{clean_text}');
        utterance.pitch = 0.85; utterance.rate = 1.1;
        synth.speak(utterance);
        </script>
    """, height=0)

# --- 4. RENDER INTERFACE ---
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
    <div class="aegis-data-stream">
        <p class="title">AEGIS // MARK I CORE</p>
        <p class="status">USER: IKKI | LOC: TIRUCHIRAPPALLI | STATUS: ONLINE</p>
    </div>
</div>
''', unsafe_allow_html=True)

# 3D Projection (Spider-Logo Area)
if THREE_LINK:
    with st.container():
        st.markdown('<div class="projection-orb">', unsafe_allow_html=True)
        threejs_component(
            model_url="https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF/Duck.gltf",
            height=280, width=280, rotation_speed=0.01
        )
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. CHAT ENGINE ---
if "log" not in st.session_state: st.session_state.log = []

for m in st.session_state.log:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if cmd := st.chat_input("Input Command..."):
    st.session_state.log.append({"role": "user", "content": cmd})
    with st.chat_message("user"): st.markdown(cmd)

    with st.chat_message("assistant"):
        with st.spinner("SYNAPSING..."):
            intel = get_aegis_intel(cmd)
            st.markdown(intel)
            speak(intel)
            st.session_state.log.append({"role": "assistant", "content": intel})

# Update Loop
time.sleep(2)
st.rerun()
