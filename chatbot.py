import streamlit as st
import psutil
import time
from groq import Groq
from streamlit_threejs import threejs_component

# --- 1. CORE CONFIG & THEME ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# --- 2. HOLOGRAPHIC UI (STARK CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    /* Global Dark Mode Stark Theme */
    .stApp {
        background-color: #060b10;
        color: #00d4ff;
        font-family: 'Orbitron', sans-serif;
    }

    /* Prevent overlap: Push chat below the HUD */
    .block-container { padding-top: 160px !important; }
    header, footer, #MainMenu { visibility: hidden; }

    /* Floating Header: Circle + Info Block */
    .aegis-header-container {
        position: fixed;
        top: 20px;
        left: 30px;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 25px;
        pointer-events: none;
    }

    .aegis-info-block {
        border-left: 3px solid #00d4ff;
        padding-left: 20px;
    }

    .title-text { font-size: 1.5rem; font-weight: bold; text-shadow: 0 0 10px #00d4ff; margin: 0; }
    .sub-text { font-size: 0.7rem; opacity: 0.8; margin: 5px 0 0 0; }
    
    /* Gauge Animation */
    .ring-circle { transition: stroke-dashoffset 0.8s ease; transform: rotate(-90deg); transform-origin: center; }

    /* 3D Model Positioning (Bottom Right) */
    .floating-3d-zone {
        position: fixed;
        bottom: 40px;
        right: 40px;
        z-index: 1000;
        pointer-events: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. NEURAL LINK (GROQ LLAMA 3.3) ---
# Ensure your key is in Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_aegis_response(user_input):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are AEGIS, a high-tech AI interface for Ikki. Location: Tiruchirappalli. Personality: Sophisticated, Stark-Industries style. You are an expert in Physics and Python. Respond concisely but intelligently."
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Neural Link Error: {str(e)}"

# --- 4. SPEECH CORE ---
def speak_response(text):
    """Browser-based text-to-speech for the J.A.R.V.I.S. voice"""
    clean_text = text.replace("'", "\\'")
    js_code = f"""
        <script>
        var speech = new SpeechSynthesisUtterance('{clean_text}');
        speech.rate = 1.05; 
        speech.pitch = 0.85; 
        window.speechSynthesis.speak(speech);
        </script>
    """
    st.components.v1.html(js_code, height=0)

# --- 5. UI COMPONENTS ---
def render_hud():
    integrity = 100 - psutil.cpu_percent()
    circum = 502
    offset = circum - (integrity / 100) * circum
    color = "#ff4b2b" if integrity < 30 else "#00d4ff"
    
    hud_html = f'''
    <div class="aegis-header-container">
        <div style="position: relative; width: 120px; height: 120px;">
            <svg width="120" height="120" viewBox="0 0 220 220">
                <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
                <circle class="ring-circle" stroke="{color}" stroke-width="12" 
                        stroke-dasharray="{circum}" stroke-dashoffset="{offset}" 
                        stroke-linecap="round" fill="transparent" r="80" cx="110" cy="110"
                        style="filter: drop-shadow(0 0 8px {color});"/>
            </svg>
            <div style="position: absolute; top: 40px; left: 0; width: 100%; text-align: center;">
                <div style="color: {color}; font-size: 1.2rem; font-weight: bold;">{int(integrity)}%</div>
                <div style="color: {color}; font-size: 0.4rem; letter-spacing: 1px;">CORE</div>
            </div>
        </div>
        <div class="aegis-info-block">
            <p class="title-text">AEGIS // NEURAL INTERFACE</p>
            <p class="sub-text">USER: IKKI | LOC: TIRUCHIRAPPALLI | STATUS: ACTIVE</p>
        </div>
    </div>
    '''
    st.markdown(hud_html, unsafe_allow_html=True)

def render_3d_projection():
    with st.container():
        st.markdown('<div class="floating-3d-zone">', unsafe_allow_html=True)
        # Using a default GLTF model; swap URL for your custom Spider-Man logo
        threejs_component(
            model_url="https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF/Duck.gltf",
            height=250, width=250, rotation_speed=0.015
        )
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. MAIN EXECUTION ---
render_hud()
render_3d_projection()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("PROCESSING NEURAL DATA..."):
            response = get_aegis_response(prompt)
            st.markdown(response)
            speak_response(response) # Trigger Voice
            st.session_state.messages.append({"role": "assistant", "content": response})

# Auto-Refresh to animate the HUD gauge
time.sleep(2)
st.rerun()
