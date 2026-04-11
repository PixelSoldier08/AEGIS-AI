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

# --- 2. THE TOTAL HUD & CAPSULE OVERRIDE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }

    /* === CIRCULAR HUD RESTORATION === */
    .aegis-hud-circle {
        position: fixed; top: 25px; left: 40px; z-index: 10000;
        display: flex; align-items: center; gap: 15px;
    }
    .hud-ring {
        width: 60px; height: 60px;
        border: 3px solid #00d4ff;
        border-top: 3px solid transparent;
        border-radius: 50%;
        animation: spin 2s linear infinite;
        filter: drop-shadow(0 0 5px #00d4ff);
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    /* === THE FINAL CAPSULE FIX === */
    /* This kills the grey box background entirely */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
        position: fixed !important;
        bottom: 30px !important;
        padding: 0 !important;
    }

    /* This targets the inner container that forces the square shape */
    [data-testid="stChatInput"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* The actual Capsule Body */
    [data-testid="stChatInput"] textarea {
        background: rgba(0, 212, 255, 0.07) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 100px !important; 
        color: #00d4ff !important;
        padding: 14px 60px 14px 25px !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2) !important;
        height: 55px !important;
        min-height: 55px !important;
    }

    /* Centering the Enter Button inside the Capsule */
    [data-testid="stChatInput"] button {
        background-color: transparent !important;
        border: none !important;
        color: #00d4ff !important;
        right: 15px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stChatInput"] button:hover {
        color: #fff !important;
        filter: drop-shadow(0 0 8px #00d4ff);
    }
    </style>

    <div class="aegis-hud-circle">
        <div class="hud-ring"></div>
        <div>
            <h2 style="margin:0; font-size: 1.1rem; letter-spacing: 2px;">AEGIS // MARK I</h2>
            <p style="margin:0; font-size: 0.6rem; opacity: 0.6;">OPERATOR: IKKI</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. 3D & CHAT LOGIC ---
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
    <div style="position: fixed; bottom: 120px; right: 40px; z-index: 10000;">
        <iframe srcdoc='
            <html>
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <body style="margin:0; background:transparent;">
                <model-viewer src="{model_uri}" auto-rotate rotation-speed="30deg" 
                    camera-controls disable-zoom exposure="1.3"
                    style="width:280px; height:280px; background:transparent; outline:none;">
                </model-viewer>
            </body>
            </html>
        ' style="width:280px; height:280px; border:none;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Message display
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Assistant processing here
    st.rerun()
