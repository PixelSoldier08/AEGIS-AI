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

# Secure Client Initialization
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. THE TOTAL INTERFACE OVERRIDE ---
# Note: CSS curly braces are doubled {{ }} to prevent Python f-string errors.
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {{
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
    }}

    /* 1. THE ULTIMATE SPACE & BORDER KILLER */
    .main .block-container {{
        padding-bottom: 0px !important;
        margin-bottom: 0px !important;
    }}

    /* This removes the "border-like structure" you see around the input */
    div[data-testid="stChatInput"] {{
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 0px !important;
        position: fixed !important;
        bottom: 20px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 10001 !important;
    }}

    /* This targets the inner wrapper that usually holds the grey border */
    div[data-testid="stChatInput"] > div {{
        border: none !important;
        background: transparent !important;
        padding: 0px !important;
    }}

    /* 2. THE CAPSULE DESIGN (Inner only) */
    div[data-testid="stChatInput"] textarea {{
        background: rgba(0, 212, 255, 0.1) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 50px !important; 
        color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
    }}

    /* 3. STARFIELD & HUD */
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

    header, footer {{visibility: hidden !important;}}
    </style>

    <div class="stars"></div>
""", unsafe_allow_html=True)

# --- 3. 3D HOLOGRAM PROJECTION ---
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
    <div style="position: fixed; bottom: 100px; right: 30px; z-index: 10000;">
        <iframe srcdoc='
            <html>
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <body style="margin:0; background:transparent; overflow:hidden;">
                <model-viewer src="{model_uri}" auto-rotate rotation-speed="40deg" 
                    camera-controls disable-zoom exposure="1.5"
                    style="width:300px; height:300px; background:transparent; outline:none;">
                </model-viewer>
            </body>
            </html>
        ' style="width:300px; height:300px; border:none;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. SYSTEM CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vertical offset for the top HUD
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Bottom buffer to prevent overlap
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

if prompt := st.chat_input("Input command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are AEGIS. Respond to {USER_NAME} in {LOCATION}. Maintain a high-tech, helpful persona."},
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
