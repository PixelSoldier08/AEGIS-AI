import streamlit as st
import psutil
from groq import Groq
import base64
import os

# --- 1. BOOT SEQUENCE ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. THE DATA INJECTOR (With Debugging) ---
def get_model_uri(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            return f"data:application/octet-stream;base64,{b64}", "SUCCESS: File Loaded Locally"
        except Exception as e:
            return None, f"ERROR: Could not read file - {e}"
    else:
        return None, f"ERROR: File '{file_name}' not found in directory."

# Initialize URI and check status
model_uri, debug_msg = get_model_uri("download.glb")

# --- 3. HOLOGRAPHIC INTERFACE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container { padding-top: 150px !important; }

    .projection-zone {
        position: fixed; bottom: 30px; right: 30px; z-index: 9999;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }
    .debug-text { color: #555; font-size: 10px; position: fixed; bottom: 5px; left: 5px; }
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

    # 3D Hologram - Only renders if the file was found
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
                        camera-controls disable-zoom 
                        exposure="1.3" shadow-intensity="1"
                        style="width: 320px; height: 320px; background: transparent; outline: none;">
                    </model-viewer>
                </body>
                </html>
            ' style="width: 320px; height: 320px; border: none; background: transparent;"></iframe>
        </div>
        ''', unsafe_allow_html=True)
    else:
        # If file is missing, show a warning in the projection zone
        st.markdown(f'''<div class="projection-zone" style="display:flex; align-items:center; justify-content:center; color:red; font-size:12px; text-align:center;">
            DATA LINK SEVERED:<br>{debug_msg}</div>''', unsafe_allow_html=True)

# --- 5. EXECUTION ---
render_ui()
st.markdown(f'<div class="debug-text">System Debug: {debug_msg}</div>', unsafe_allow_html=True)

if cmd := st.chat_input("Command AEGIS..."):
    with st.chat_message("user"):
        st.write(cmd)
    # Chat logic remains same...
