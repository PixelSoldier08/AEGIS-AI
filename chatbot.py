import streamlit as st
import psutil
import requests
import base64
from groq import Groq

# --- 1. CORE IDENTITY & CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# Permanent Identity Lock
USER_NAME = "Ikki"
LOCATION = "Tiruchirappalli"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. STABLE 3D DATA LINK ---
@st.cache_data
def get_aegis_model():
    # Direct Raw access to ensure 3D data flows correctly
    url = "https://raw.githubusercontent.com/PixelSoldier08/AEGIS-AI/main/download.glb"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return f"data:application/octet-stream;base64,{base64.b64encode(res.content).decode()}"
    except:
        return None
    return None

model_uri = get_aegis_model()

# --- 3. REINFORCED HUD DESIGN ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {{ background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }}
    
    /* Force HUD Visibility */
    .aegis-hud {{
        position: fixed; top: 20px; left: 30px; z-index: 10000;
        padding: 15px; border-left: 3px solid #00d4ff;
        background: rgba(0, 212, 255, 0.05);
    }}
    
    /* 3D Hologram Positioning */
    .hologram-container {{
        position: fixed; bottom: 20px; right: 20px; z-index: 10000;
        width: 300px; height: 300px;
    }}
    
    /* Clean UI */
    header, footer, #MainMenu {{ visibility: hidden; }}
    .stChatMessage {{ background: rgba(0, 212, 255, 0.05) !important; border: 1px solid #00d4ff33 !important; }}
    </style>
    
    <div class="aegis-hud">
        <h2 style="margin:0; font-size: 1.2rem; letter-spacing: 2px;">AEGIS // MARK I</h2>
        <p style="margin:0; font-size: 0.7rem; color: #00d4ff; opacity: 0.7;">OPERATOR: {USER_NAME.upper()} | LOC: {LOCATION.upper()}</p>
    </div>
""", unsafe_allow_html=True)

# --- 4. SPEECH SYNTHESIS ---
def speak(text):
    if text:
        clean_text = text.replace("'", "\\'").replace("\n", " ")
        st.components.v1.html(f"""
            <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{clean_text}');
            msg.pitch = 0.9; msg.rate = 1.0;
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)

# --- 5. INTERFACE & 3D ---
if model_uri:
    st.markdown(f'''
    <div class="hologram-container">
        <iframe srcdoc='
            <html>
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <body style="margin:0; background:transparent; overflow:hidden;">
                <model-viewer src="{model_uri}" auto-rotate rotation-speed="30deg" 
                    camera-controls disable-zoom exposure="1.2"
                    style="width:300px; height:300px; background:transparent; outline:none;">
                </model-viewer>
            </body>
            </html>
        ' style="width:300px; height:300px; border:none;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 6. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Input command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Identity injected directly into every request
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are AEGIS, a high-tech AI. You are talking to {USER_NAME} in {LOCATION}. Be brief, professional, and slightly futuristic."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile"
            )
            full_res = response.choices[0].message.content
            st.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            speak(full_res)
        except Exception as e:
            st.error(f"SYSTEM FAILURE: {e}")
