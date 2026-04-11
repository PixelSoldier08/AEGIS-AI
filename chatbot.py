import streamlit as st
import psutil
import requests
import base64
from groq import Groq

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. MOTION BACKGROUND & INTERFACE OVERRIDE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* ANIMATED MOTION BACKGROUND */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        overflow: hidden;
        color: #00d4ff;
        font-family: 'Orbitron', sans-serif;
    }

    /* Star Layers */
    @keyframes moveStars {
        from { transform: translateY(0px); }
        to { transform: translateY(-2000px); }
    }

    .stars {
        position: fixed; top: 0; left: 0; width: 100%; height: 2000px;
        background: transparent url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        z-index: -1;
        animation: moveStars 100s linear infinite;
        opacity: 0.3;
    }

    header, footer, #MainMenu { visibility: hidden; }

    /* === DUAL-LAYER HUD RING === */
    .aegis-hud-container {
        position: fixed; top: 25px; left: 40px; z-index: 10000;
        display: flex; align-items: center; gap: 20px;
    }
    .hud-ring-outer {
        width: 70px; height: 70px;
        border: 2px dashed #00d4ff;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        animation: spin-slow 8s linear infinite;
    }
    .hud-ring-inner {
        width: 45px; height: 45px;
        border: 3px solid #00d4ff;
        border-top: 3px solid transparent;
        border-radius: 50%;
        animation: spin-fast 1.5s linear infinite;
    }
    @keyframes spin-slow { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes spin-fast { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

    /* === CAPSULE FIX (STABLE) === */
    div[data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
        position: fixed !important;
        bottom: 40px !important;
        z-index: 10001 !important;
    }

    div[data-testid="stChatInput"] > div {
        background-color: transparent !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: rgba(0, 212, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.4) !important;
        border-radius: 100px !important; 
        color: #00d4ff !important;
        padding: 12px 60px 12px 25px !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.1) !important;
    }

    div[data-testid="stChatInput"] button {
        background-color: transparent !important;
        color: #00d4ff !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        right: 15px !important;
    }
    </style>

    <div class="stars"></div>
    
    <div class="aegis-hud-container">
        <div class="hud-ring-outer">
            <div class="hud-ring-inner"></div>
        </div>
        <div>
            <h2 style="margin:0; font-size: 1.2rem; letter-spacing: 2px;">AEGIS // MARK I</h2>
            <p style="margin:0; font-size: 0.6rem; opacity: 0.6;">OPERATOR: IKKI | STATUS: KINETIC</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. 3D PROJECTION ---
@st.cache_data
def get_aegis_model():
    url = "https://raw.githubusercontent.com/PixelSoldier08/AEGIS-AI/main/download.glb"
    try:
        res = requests.get(url, timeout=10)
        return f"data:application/octet-stream;base64,{base64.b64encode(res.content).decode()}"
    except: return None

model_uri = get_aegis_model()

if model_uri:
    st.markdown(f'''
    <div style="position: fixed; bottom: 130px; right: 40px; z-index: 10000;">
        <iframe srcdoc='
            <html>
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <body style="margin:0; background:transparent; overflow:hidden;">
                <model-viewer src="{model_uri}" auto-rotate rotation-speed="30deg" 
                    camera-controls disable-zoom exposure="1.3"
                    style="width:280px; height:280px; background:transparent; outline:none;">
                </model-viewer>
            </body>
            </html>
        ' style="width:280px; height:280px; border:none;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. CHAT SYSTEM ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Spacer for HUD
st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are AEGIS. Respond like a futuristic AI."},
                          {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except: st.error("Neural Link Failed.")
    st.rerun()
