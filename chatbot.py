import streamlit as st
import requests
import base64
from groq import Groq

# --- 1. CORE SYSTEM ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide")

USER_NAME = "Ikki"
LOCATION = "Tiruchirappalli"

# Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. THE INTERFACE (NO CRASH VERSION) ---
css_code = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
    }

    .stApp {
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Fixed Input Box at Bottom */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 20px !important;
        z-index: 1000;
        background: transparent !important;
    }

    /* Top Left HUD */
    .aegis-hud {
        position: fixed; top: 10px; left: 20px; z-index: 1001;
        border-left: 3px solid #ff0000; /* Red Tactical Accent */
        padding-left: 15px;
    }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# UI Widgets
st.markdown(f'''
    <div class="aegis-hud">
        <h2 style="margin:0; font-size: 1.1rem; color:#ff0000; letter-spacing:2px;">AEGIS // MK I</h2>
        <p style="margin:0; font-size: 0.7rem; color:#00d4ff;">OPERATOR: {USER_NAME.upper()}</p>
        <p style="margin:0; font-size: 0.6rem; opacity:0.6; color:#00d4ff;">LOC: {LOCATION.upper()}</p>
    </div>
''', unsafe_allow_html=True)

# --- 3. THE BLOOD SPIDER (Red & Transparent) ---
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
    <div style="position: fixed; bottom: 80px; right: 20px; z-index: 999;">
        <iframe srcdoc='
            <html>
            <head>
                <style>
                    html, body {{ background: transparent !important; margin: 0; overflow: hidden; }}
                    model-viewer {{
                        width: 300px; height: 300px; 
                        background-color: transparent !important;
                        filter: brightness(0.7) sepia(1) hue-rotate(-50deg) saturate(12) contrast(1.2);
                        --background-color: transparent !important;
                    }}
                </style>
            </head>
            <body>
                <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
                <model-viewer src="{model_uri}" auto-rotate camera-controls disable-zoom
                    shadow-intensity="2" environment-intensity="0.2" exposure="0.8">
                </model-viewer>
            </body>
            </html>
        ' style="width:300px; height:300px; border:none; background:transparent;" allowtransparency="true"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. THE BRAIN (Groq + Identity) ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # HARDCODING BRAIN CONTENT HERE
            system_msg = {
                "role": "system", 
                "content": f"You are AEGIS, a high-security tactical AI. Your operator is {USER_NAME}. "
                           f"You are currently deployed in {LOCATION}. Respond with tactical brevity."
            }
            
            response = client.chat.completions.create(
                messages=[system_msg, *st.session_state.messages],
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"NEURAL ERROR: {e}")
    st.rerun()
