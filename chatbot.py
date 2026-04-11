import streamlit as st
import requests
import base64
from groq import Groq

# --- 1. SYSTEM CORE ---
st.set_page_config(
    page_title="AEGIS MARK I", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

USER_NAME = "Ikki"
LOCATION = "Tiruchirappalli"

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. THE NUCLEAR INTERFACE OVERRIDE ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* KILL ALL DEFAULT PADDING & SCROLLBAR GAPS */
    html, body, [data-testid="stAppViewContainer"] {{
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        overflow: hidden !important;
        height: 100vh !important;
    }}

    .main .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
    }}

    /* HIDE HEADER/FOOTER AND BLACK BARS */
    header, footer, [data-testid="stHeader"], [data-testid="stBottom"] {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* CHAT INPUT STABILIZATION - Removes the grey structure */
    div[data-testid="stChatInput"] {{
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        background: transparent !important;
        border: none !important;
        width: 60% !important;
        z-index: 10000 !important;
    }}

    div[data-testid="stChatInput"] > div {{
        background: transparent !important;
        border: none !important;
    }}

    div[data-testid="stChatInput"] textarea {{
        background: rgba(0, 212, 255, 0.1) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 50px !important; 
        color: #00d4ff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4) !important;
    }}

    /* HUD */
    .aegis-hud {{
        position: fixed; top: 20px; left: 30px; z-index: 10001;
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff;
    }}
    </style>
    <div class="aegis-hud">
        <h2 style="margin:0; font-size: 1.2rem; letter-spacing: 3px;">AEGIS // MK I</h2>
        <p style="margin:0; font-size: 0.6rem; opacity: 0.6;">LOC: {LOCATION.upper()}</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. 3D HOLOGRAM (ULTIMATE TRANSPARENCY FIX) ---
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
    <div style="position: fixed; bottom: 100px; right: 20px; z-index: 10002;">
        <iframe srcdoc='
            <html>
            <head>
                <style>
                    html, body {{ background: transparent !important; margin: 0; overflow: hidden; }}
                    model-viewer {{ 
                        width: 300px; height: 300px; 
                        background-color: transparent !important;
                        --background-color: transparent !important;
                    }}
                </style>
            </head>
            <body>
                <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
                <model-viewer src="{model_uri}" auto-rotate camera-controls disable-zoom></model-viewer>
            </body>
            </html>
        ' style="width:300px; height:300px; border:none; background:transparent;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. CHAT AREA ---
# Container for messages to prevent them from hitting the edges
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AEGIS, a high-tech AI. Respond concisely."},
                    *st.session_state.messages
                ],
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.write(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"SYSTEM ERROR: {e}")
    st.rerun()
