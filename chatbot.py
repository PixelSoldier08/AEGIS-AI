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

# User Identity Parameters
USER_NAME = "Ikki"
LOCATION = "Tiruchirappalli"

# Initialize AI Link
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. THE STABILIZED INTERFACE ---
# Doubled curly braces {{ }} prevent the script from crashing.
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* 1. KINETIC THEME */
    .stApp {{
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
    }}

    /* 2. KILL THE "STRUCTURE" BORDERS */
    /* This targets the grey box you hate and makes it invisible */
    [data-testid="stChatInput"] {{
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        padding-bottom: 30px !important;
    }}

    [data-testid="stChatInput"] > div {{
        background-color: transparent !important;
        border: none !important;
    }}

    /* 3. THE CAPSULE DESIGN */
    [data-testid="stChatInput"] textarea {{
        background: rgba(0, 212, 255, 0.1) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 50px !important; 
        color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2) !important;
        padding-left: 20px !important;
    }}

    /* 4. CHAT BUBBLES - FIXING THE "LONG BOX" LOOK */
    .stChatMessage {{
        background: rgba(0, 212, 255, 0.05) !important;
        border-left: 3px solid #00d4ff !important;
        border-radius: 0 15px 15px 0 !important;
        max-width: 80% !important; /* Prevents the box from being too long */
        margin-bottom: 20px !important;
    }}

    /* 5. HUD ELEMENTS */
    header, footer, [data-testid="stHeader"] {{ visibility: hidden !important; }}

    .aegis-hud {{
        position: fixed; top: 20px; left: 30px; z-index: 1000;
        display: flex; align-items: center; gap: 15px;
    }}
    .ring {{
        width: 50px; height: 50px; border: 2px dashed #00d4ff; 
        border-radius: 50%; animation: spin 8s linear infinite;
    }}
    @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    </style>

    <div class="aegis-hud">
        <div class="ring"></div>
        <div>
            <h2 style="margin:0; font-size: 1rem; letter-spacing: 2px; color:#00d4ff;">AEGIS // MK I</h2>
            <p style="margin:0; font-size: 0.6rem; opacity: 0.7; color:#00d4ff;">OPERATOR: {USER_NAME.upper()}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. STABILIZED 3D HOLOGRAM (FORCE TRANSPARENCY) ---
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
    <div style="position: fixed; bottom: 80px; right: 20px; z-index: 999999; pointer-events: auto;">
        <iframe srcdoc='
            <html>
            <head>
                <style>
                    /* Force the browser to render nothing behind the model */
                    html, body {{ 
                        margin: 0; 
                        padding: 0; 
                        background: transparent !important; 
                        overflow: hidden;
                    }}
                    model-viewer {{
                        width: 300px; 
                        height: 300px; 
                        --background-color: transparent !important; /* Specific model-viewer fix */
                        background-color: transparent !important;
                        outline: none;
                    }}
                </style>
            </head>
            <body>
                <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
                <model-viewer 
                    src="{model_uri}" 
                    auto-rotate 
                    rotation-speed="30deg" 
                    camera-controls 
                    touch-action="pan-y"
                    disable-zoom="false"
                    shadow-intensity="0"
                    exposure="1.2">
                </model-viewer>
            </body>
            </html>
        ' style="width:300px; height:300px; border:none; background:transparent;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. SYSTEM LOGIC (He speaks here!) ---
# Add space so messages don't hide behind the HUD
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Spacer to ensure user can scroll past the fixed input
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

if prompt := st.chat_input("Command AEGIS..."):
    # 1. Save and show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Get and show AI response
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are AEGIS, a tactical AI assistant. You are speaking to {USER_NAME} in {LOCATION}. Use a high-tech, efficient tone."},
                    *st.session_state.messages
                ],
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.write(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"NEURAL DISCONNECT: {e}")
    
    st.rerun()
