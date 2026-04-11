import streamlit as st
import psutil
import requests
import base64
from groq import Groq

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

USER_NAME = "Ikki"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. THE CAPSULE OVERRIDE (EXACT IMAGE MATCH) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {{ background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }}
    header, footer, #MainMenu {{ visibility: hidden; }}
    
    /* === THE PRECISION CAPSULE FIX === */
    /* This targets the outer wrapper that Streamlit uses */
    [data-testid="stChatInput"] {{
        position: fixed !important;
        bottom: 40px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 650px !important; /* This controls the exact 'short' size of the capsule */
        background-color: transparent !important;
        z-index: 10001 !important;
    }}

    /* This styles the actual text box inside */
    .stChatInput textarea {{
        background: rgba(0, 212, 255, 0.08) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 100px !important; /* Perfect capsule curves */
        color: #00d4ff !important;
        padding: 15px 25px !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
    }}

    /* Remove the default Streamlit grey border/background */
    [data-testid="stChatInput"] > div {{
        background-color: transparent !important;
        border: none !important;
    }}

    .aegis-hud {{
        position: fixed; top: 20px; left: 30px; z-index: 10000;
        padding: 15px; border-left: 3px solid #00d4ff;
        background: rgba(0, 212, 255, 0.05);
    }}
    </style>
    
    <div class="aegis-hud">
        <h2 style="margin:0; font-size: 1.2rem; letter-spacing: 2px;">AEGIS // MARK I</h2>
        <p style="margin:0; font-size: 0.7rem; color: #00d4ff; opacity: 0.7;">OPERATOR: {USER_NAME.upper()} | STATUS: READY</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. SPEECH & 3D (RE-SYNCED) ---
@st.cache_data
def get_aegis_model():
    url = "https://raw.githubusercontent.com/PixelSoldier08/AEGIS-AI/main/download.glb"
    try:
        res = requests.get(url, timeout=10)
        return f"data:application/octet-stream;base64,{base64.b64encode(res.content).decode()}"
    except: return None

model_uri = get_aegis_model()

# --- 4. 3D PROJECTION ---
if model_uri:
    st.markdown(f'''
    <div style="position: fixed; bottom: 140px; right: 40px; z-index: 10000;">
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

# --- 5. CHAT SYSTEM ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Using a container with padding so messages don't get hidden behind the floating capsule
main_chat = st.container()
with main_chat:
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
