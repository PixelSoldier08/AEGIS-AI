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

# --- 2. THE TOTAL INTERFACE OVERRIDE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }

    /* === THE NUCLEAR FIX FOR THE CAPSULE === */

    /* 1. Target the outer container to remove the grey background/border */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 40px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 600px !important;
        background-color: transparent !important;
        border: none !important;
        z-index: 10001 !important;
    }

    /* 2. Target the intermediate div that Streamlit uses for the box effect */
    [data-testid="stChatInput"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* 3. Style the actual Text Area into a perfect capsule */
    [data-testid="stChatInput"] textarea {
        background: rgba(0, 212, 255, 0.07) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 100px !important; 
        color: #00d4ff !important;
        padding: 12px 60px 12px 25px !important; /* Extra right padding for the button */
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
        overflow: hidden !important;
    }

    /* 4. Force the Submit Button to sit inside the blue border */
    [data-testid="stChatInput"] button {
        position: absolute !important;
        right: 15px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        background-color: transparent !important;
        border: none !important;
        color: #00d4ff !important;
        transition: 0.3s;
    }
    
    [data-testid="stChatInput"] button:hover {
        color: #ffffff !important;
        filter: drop-shadow(0 0 5px #00d4ff);
    }

    /* 5. HUD Styling */
    .aegis-hud {
        position: fixed; top: 20px; left: 30px; z-index: 10000;
        padding: 15px; border-left: 3px solid #00d4ff;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 3D & HUD RENDER ---
@st.cache_data
def get_aegis_model():
    url = "https://raw.githubusercontent.com/PixelSoldier08/AEGIS-AI/main/download.glb"
    try:
        res = requests.get(url, timeout=10)
        return f"data:application/octet-stream;base64,{base64.b64encode(res.content).decode()}"
    except: return None

model_uri = get_aegis_model()

st.markdown('<div class="aegis-hud"><h2>AEGIS // MARK I</h2><p>OPERATOR: IKKI</p></div>', unsafe_allow_html=True)

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

# --- 4. CHAT SYSTEM ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Spacer for scrolling
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Assistant Logic
    st.rerun()
