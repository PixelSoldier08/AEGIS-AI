import streamlit as st
import requests
import base64
from groq import Groq

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide")

USER_NAME = "Ikki"

# --- 2. THE REFINED CSS (No f-string issues) ---
# We use a standard string here to avoid the SyntaxErrors you see in image_cee61a
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Target the white box specifically */
    iframe { 
        background: transparent !important; 
    }

    /* Fixed Command Box */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 30px !important;
        z-index: 1000;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- 3. THE HOLOGRAM (Forced Sync) ---
@st.cache_data
def get_aegis_model():
    url = "https://raw.githubusercontent.com/PixelSoldier08/AEGIS-AI/main/download.glb"
    try:
        res = requests.get(url, timeout=10)
        return f"data:application/octet-stream;base64,{base64.b64encode(res.content).decode()}"
    except: return None

model_uri = get_aegis_model()

if model_uri:
    # Use a raw string (r''') to prevent any escape character or f-string crashes
    model_html = f'''
    <div style="position: fixed; bottom: 80px; right: 20px; z-index: 9999;">
        <iframe srcdoc='
            <html>
            <body style="margin:0; background:transparent !important;">
                <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
                <model-viewer src="{model_uri}" style="width:300px; height:300px; background:transparent;" auto-rotate camera-controls disable-zoom></model-viewer>
            </body>
            </html>
        ' style="width:300px; height:300px; border:none; background:transparent;" allowtransparency="true"></iframe>
    </div>
    '''
    st.markdown(model_html, unsafe_allow_html=True)

# --- 4. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Command AEGIS..."):
    # Add your Groq logic here as usual
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
