import streamlit as st
import requests
import base64
from groq import Groq

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="AEGIS MARK I", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

USER_NAME = "Ikki"
LOCATION = "Tiruchirappalli"

# Secure Client Link
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. INTERFACE OVERRIDE (Stabilized) ---
# Using doubled {{ }} for CSS to avoid f-string SyntaxErrors.
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* BACKGROUND */
    .stApp {{
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
    }}

    /* KILL BOTTOM SPACE & BORDERS */
    .main .block-container {{
        padding-bottom: 0px !important;
        margin-bottom: 0px !important;
        max-width: 95% !important;
    }}

    /* HIDE DEFAULT HEADER/FOOTER */
    header, footer, [data-testid="stHeader"] {{
        visibility: hidden !important;
        height: 0px !important;
    }}

    /* HUD ELEMENTS */
    .aegis-hud {{
        position: fixed; top: 25px; left: 40px; z-index: 10000;
        display: flex; align-items: center; gap: 20px;
    }}
    .ring {{
        width: 60px; height: 60px; border: 2px dashed #00d4ff; border-radius: 50%;
        animation: spin 10s linear infinite;
    }}
    @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

    /* INPUT AREA STABILIZATION */
    /* This removes the grey 'border structure' you are seeing */
    div[data-testid="stChatInput"] {{
        border: none !important;
        background: transparent !important;
        padding-bottom: 20px !important;
    }}

    div[data-testid="stChatInput"] > div {{
        background-color: transparent !important;
        border: none !important;
    }}

    /* THE CAPSULE */
    div[data-testid="stChatInput"] textarea {{
        background: rgba(0, 212, 255, 0.1) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 50px !important; 
        color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2) !important;
    }}

    /* MESSAGE BUBBLES */
    .stChatMessage {{
        background: rgba(0, 212, 255, 0.05) !important;
        border-left: 3px solid #00d4ff !important;
        border-radius: 10px !important;
    }}
    </style>

    <div class="aegis-hud">
        <div class="ring"></div>
        <div>
            <h2 style="margin:0; font-size: 1.1rem; letter-spacing: 2px;">AEGIS // MK I</h2>
            <p style="margin:0; font-size: 0.6rem; opacity: 0.6;">LOC: {LOCATION.upper()}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. 3D HOLOGRAM ---
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
    <div style="position: fixed; bottom: 80px; right: 30px; z-index: 9999;">
        <iframe srcdoc='
            <html>
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <body style="margin:0; background:transparent;">
                <model-viewer src="{model_uri}" auto-rotate rotation-speed="40deg" 
                    disable-zoom style="width:250px; height:250px; background:transparent; outline:none;">
                </model-viewer>
            </body>
            </html>
        ' style="width:250px; height:250px; border:none;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. SYSTEM LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Spacer for HUD
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Input command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AEGIS, a futuristic tactical AI. Keep responses concise and high-tech."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"SYSTEM ERROR: {e}")
    st.rerun()
