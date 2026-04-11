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

# Identity Lock
USER_NAME = "Ikki"
LOCATION = "Tiruchirappalli"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. THE TOTAL INTERFACE OVERRIDE ---
# NOTE: All CSS curly braces are doubled {{ }} to avoid f-string SyntaxErrors.
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {{
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
        overflow: hidden !important;
    }}

    @keyframes moveStars {{
        from {{ transform: translateY(0px); }}
        to {{ transform: translateY(-2000px); }}
    }}
    .stars {{
        position: fixed; top: 0; left: 0; width: 100%; height: 2000px;
        background: transparent url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        z-index: -1;
        animation: moveStars 120s linear infinite;
        opacity: 0.3;
    }}

    .main .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
        max-width: 95% !important;
    }}
    footer {{display: none !important; visibility: hidden !important;}}
    [data-testid="stHeader"] {{display: none !important;}}

    .aegis-hud-container {{
        position: fixed; top: 25px; left: 40px; z-index: 10000;
        display: flex; align-items: center; gap: 20px;
    }}
    .hud-ring-outer {{
        width: 70px; height: 70px;
        border: 2px dashed #00d4ff;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        animation: spin-slow 10s linear infinite;
    }}
    .hud-ring-inner {{
        width: 45px; height: 45px;
        border: 3px solid #00d4ff;
        border-top: 3px solid transparent;
        border-radius: 50%;
        animation: spin-fast 2s linear infinite;
    }}
    @keyframes spin-slow {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    @keyframes spin-fast {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

    div[data-testid="stChatInput"] {{
        background-color: transparent !important;
        border: none !important;
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 600px !important;
        padding: 0 !important;
        z-index: 10001 !important;
    }}

    div[data-testid="stChatInput"] > div {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    div[data-testid="stChatInput"] textarea {{
        background: rgba(0, 212, 255, 0.08) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 100px !important; 
        color: #00d4ff !important;
        padding: 12px 60px 12px 25px !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2) !important;
        line-height: 1.6 !important;
        height: 55px !important;
    }}

    div[data-testid="stChatInput"] button {{
        background-color: transparent !important;
        color: #00d4ff !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        right: 15px !important;
    }}

    .stChatMessage {{
        background: rgba(0, 212, 255, 0.03) !important;
        border-left: 3px solid #00d4ff !important;
        border-radius: 0 15px 15px 0 !important;
        margin-bottom: 10px !important;
    }}
    </style>

    <div class="stars"></div>
    
    <div class="aegis-hud-container">
        <div class="hud-ring-outer">
            <div class="hud-ring-inner"></div>
        </div>
        <div>
            <h2 style="margin:0; font-size: 1.2rem; letter-spacing: 2px;">AEGIS // MARK I</h2>
            <p style="margin:0; font-size: 0.6rem; opacity: 0.6;">OPERATOR: {USER_NAME.upper()} | STATUS: ONLINE</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. 3D PROJECTION ---
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
    <div style="position: fixed; bottom: 120px; right: 40px; z-index: 10000;">
        <iframe srcdoc='
            <html>
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <body style="margin:0; background:transparent; overflow:hidden;">
                <model-viewer src="{model_uri}" auto-rotate rotation-speed="30deg" 
                    camera-controls disable-zoom exposure="1.3" shadow-intensity="1"
                    style="width:280px; height:280px; background:transparent; outline:none;">
                </model-viewer>
            </body>
            </html>
        ' style="width:280px; height:280px; border:none;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Spacers
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are AEGIS, a futuristic AI. The operator is {USER_NAME} in {LOCATION}."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"NEURAL ERROR: {e}")
    st.rerun()
