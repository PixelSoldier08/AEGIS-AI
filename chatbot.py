import streamlit as st
import requests
import base64
from groq import Groq

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide")

USER_NAME = "Ikki"
LOCATION = "Tiruchirappalli"

# Initialize Session State for Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. STABLE UI INJECTION (Fixes the Crash) ---
# We use a standard string here to avoid f-string quote conflicts
css_code = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Fixed Command Box Positioning */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 30px !important;
        z-index: 1000;
    }

    /* Top HUD Styling */
    .aegis-hud {
        position: fixed; top: 20px; left: 30px; z-index: 1001;
        border-left: 2px solid #00d4ff;
        padding-left: 15px;
    }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# HUD Display
st.markdown(f'''
    <div class="aegis-hud">
        <h2 style="margin:0; font-size: 1.2rem; letter-spacing: 2px; color:#00d4ff;">AEGIS // MK I</h2>
        <p style="margin:0; font-size: 0.7rem; opacity: 0.7; color:#00d4ff;">OPERATOR: {USER_NAME}</p>
        <p style="margin:0; font-size: 0.6rem; opacity: 0.5; color:#00d4ff;">LOC: {LOCATION}</p>
    </div>
''', unsafe_allow_html=True)

# --- 3. 3D HOLOGRAM (Transparency Patch) ---
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
    <div style="position: fixed; bottom: 100px; right: 20px; z-index: 999;">
        <iframe srcdoc='
            <html>
            <body style="margin:0; background:transparent;">
                <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
                <model-viewer src="{model_uri}" style="width:300px; height:300px; background:transparent;" 
                    auto-rotate camera-controls disable-zoom></model-viewer>
            </body>
            </html>
        ' style="width:300px; height:300px; border:none; background:transparent;" allowtransparency="true"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. CHAT FUNCTIONALITY ---
# Display conversation history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Command AEGIS..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AEGIS, a tactical assistant. Use concise, high-tech language."},
                    *st.session_state.messages
                ],
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"NEURAL DISCONNECT: {e}")
    
    st.rerun()
