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

# --- 2. THE REFINED INTERFACE ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* CORE THEME */
    .stApp {{
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
    }}

    /* FIXING THE COMMAND BOX (Bringing it back) */
    div[data-testid="stChatInput"] {{
        position: fixed !important;
        bottom: 20px !important;
        padding: 0 10% !important;
        z-index: 10000 !important;
    }}

    div[data-testid="stChatInput"] textarea {{
        background: rgba(0, 212, 255, 0.1) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 50px !important; 
        color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
    }}

    /* HIDING THE GREY BOX STRUCTURE AROUND INPUT */
    div[data-testid="stChatInput"] > div {{
        background-color: transparent !important;
        border: none !important;
    }}

    /* HUD ELEMENTS */
    header, footer, [data-testid="stHeader"] {{ visibility: hidden !important; }}

    .aegis-hud {{
        position: fixed; top: 20px; left: 30px; z-index: 1000;
        color: #00d4ff;
    }}
    </style>
    <div class="aegis-hud">
        <h2 style="margin:0; font-size: 1.1rem; letter-spacing: 2px;">AEGIS // MK I</h2>
        <p style="margin:0; font-size: 0.6rem; opacity: 0.7;">OPERATOR: {USER_NAME.upper()}</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. THE "WHITE BOX" KILLER (3D Model) ---
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
    <div style="position: fixed; bottom: 80px; right: 20px; z-index: 9999; pointer-events: auto;">
        <iframe srcdoc='
            <html>
            <head>
                <style>
                    /* Force everything to be transparent */
                    html, body {{ 
                        background: transparent !important; 
                        margin: 0; 
                        padding: 0; 
                        overflow: hidden; 
                    }}
                    model-viewer {{
                        width: 300px; 
                        height: 300px; 
                        background-color: transparent !important;
                        --background-color: transparent !important;
                        outline: none;
                    }}
                </style>
            </head>
            <body>
                <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
                <model-viewer 
                    src="{model_uri}" 
                    auto-rotate 
                    camera-controls 
                    touch-action="pan-y"
                    shadow-intensity="0"
                    exposure="1">
                </model-viewer>
            </body>
            </html>
        ' style="width:300px; height:300px; border:none; background:transparent;" allowtransparency="true"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. CHAT LOGIC ---
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)

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
                    {"role": "system", "content": f"You are AEGIS. Respond to {USER_NAME}."},
                    *st.session_state.messages
                ],
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.write(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"NEURAL ERROR: {e}")
    st.rerun()
