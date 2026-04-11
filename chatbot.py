import streamlit as st
import psutil
import requests
import base64
from groq import Groq

# --- 1. BOOT SEQUENCE ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# Establish Neural Link
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. THE REMOTE DATA INJECTOR ---
@st.cache_data # This keeps the model in memory so it doesn't download every second
def get_remote_model():
    # DIRECT RAW LINK to bypass all GitHub blocks
    url = "https://raw.githubusercontent.com/PixelSoldier08/AEGIS-AI/main/download.glb"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            b64 = base64.b64encode(response.content).decode()
            return f"data:application/octet-stream;base64,{b64}"
        else:
            return None
    except:
        return None

model_uri = get_remote_model()

# --- 3. INTERFACE DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container { padding: 0 !important; }

    .projection-zone {
        position: fixed; bottom: 30px; right: 30px; z-index: 9999;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. HUD & 3D RENDERING ---
def render_ui():
    # HUD Header
    st.markdown('''
        <div style="position: fixed; top: 25px; left: 40px; border-left: 2px solid #00d4ff; padding-left: 20px;">
            <p style="font-size: 1.5rem; font-weight: bold; margin: 0;">AEGIS // MARK I</p>
            <p style="font-size: 0.7rem; opacity: 0.8; margin: 0;">USER: IKKI | STATUS: ACTIVE</p>
        </div>
    ''', unsafe_allow_html=True)

    # 3D Hologram
    if model_uri:
        st.markdown(f'''
        <div class="projection-zone">
            <iframe srcdoc='
                <html>
                <head>
                    <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
                </head>
                <body style="margin: 0; background: transparent; overflow: hidden;">
                    <model-viewer src="{model_uri}" auto-rotate rotation-speed="40deg" 
                        camera-controls disable-zoom exposure="1.3"
                        style="width: 320px; height: 320px; background: transparent; outline: none;">
                    </model-viewer>
                </body>
                </html>
            ' style="width: 320px; height: 320px; border: none; background: transparent;"></iframe>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.error("AEGIS CORE OFFLINE: Could not fetch 3D Data.")

# --- 5. CHAT ENGINE ---
render_ui()

if "history" not in st.session_state:
    st.session_state.history = []

# Display Chat
for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Command Input
if cmd := st.chat_input("Command AEGIS..."):
    st.session_state.history.append({"role": "user", "content": cmd})
    with st.chat_message("user"):
        st.markdown(cmd)
    
    with st.chat_message("assistant"):
        try:
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": cmd}],
                model="llama-3.3-70b-versatile"
            )
            ans = chat.choices[0].message.content
            st.markdown(ans)
            st.session_state.history.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Neural Error: {e}")
