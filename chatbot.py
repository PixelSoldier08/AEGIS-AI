import streamlit as st
import psutil
import requests
import base64
from groq import Groq

# --- 1. BOOT ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. THE NUCLEAR CSS OVERRIDE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }

    /* 1. Remove the grey background and default border from the Streamlit wrapper */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 80% !important;
        max-width: 600px !important;
        background-color: transparent !important;
        border: none !important;
        z-index: 10001 !important;
    }

    /* 2. Style the actual input box */
    [data-testid="stChatInput"] textarea {
        background: rgba(0, 212, 255, 0.07) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 100px !important; /* Forces the capsule shape */
        color: #00d4ff !important;
        padding-top: 12px !important;
        padding-bottom: 12px !important;
        padding-left: 25px !important;
        padding-right: 50px !important; /* Space for the enter button */
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
        line-height: 1.5 !important;
    }

    /* 3. Force the Enter/Submit button to be INSIDE the capsule */
    [data-testid="stChatInput"] button {
        right: 15px !important;
        bottom: 8px !important;
        background-color: transparent !important;
        color: #00d4ff !important;
    }

    /* 4. Hide the annoying grey box that Streamlit puts behind the input */
    [data-testid="stChatInput"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

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

# Spacer to prevent chat from going under the input
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Assistant logic here
    st.rerun()
