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
        width: 50px; height: 50px;
        border: 3px solid #00d4ff;
        border-top: 3px solid transparent;
        border-radius: 50%;
        animation: spin-fast 1.5s linear infinite;
    }
    @keyframes spin-slow { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    @keyframes spin-fast { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    /* === THE CAPSULE FIX (VERSION 7.0) === */
    /* This completely hides the 'Box' wrapper */
    div[data-testid="stChatInput"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        position: fixed !important;
        bottom: 40px !important;
    }

    /* Target the inner div to stop the grey background */
    div[data-testid="stChatInput"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* The actual Capsule Body */
    div[data-testid="stChatInput"] textarea {
        background: rgba(0, 212, 255, 0.07) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 100px !important; 
        color: #00d4ff !important;
        padding: 12px 60px 12px 25px !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.25) !important;
        line-height: 1.6 !important;
    }

    /* Center the Send Button inside the Capsule */
    div[data-testid="stChatInput"] button {
        background-color: transparent !important;
        color: #00d4ff !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        right: 15px !important;
    }
    
    div[data-testid="stChatInput"] button:hover {
        color: #fff !important;
        filter: drop-shadow(0 0 8px #00d4ff);
    }
    </style>

    <div class="aegis-hud-container">
        <div class="hud-ring-outer">
            <div class="hud-ring-inner"></div>
        </div>
        <div>
            <h2 style="margin:0; font-size: 1.2rem; letter-spacing: 2px;">AEGIS // MARK I</h2>
            <p style="margin:0; font-size: 0.6rem; opacity: 0.6;">OPERATOR: IKKI | STATUS: ACTIVE</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. 3D & CHAT ENGINE ---
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

if "messages" not in st.session_state:
    st.session_state.messages = []

# Spacer
st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are AEGIS. Be brief."},
                          {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except: st.error("Neural Link Failed.")
    st.rerun()
