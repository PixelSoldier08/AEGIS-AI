import streamlit as st
import psutil
import requests
import base64
from groq import Groq

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

USER_NAME = "Ikki"
LOCATION = "Tiruchirappalli"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. HOLOGRAPHIC STYLING (TYPING AREA UPDATE) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* Clean UI Overrides */
    .stApp {{ background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }}
    header, footer, #MainMenu {{ visibility: hidden; }}
    
    /* HUD Header (Left Side) */
    .aegis-hud {{
        position: fixed; top: 20px; left: 30px; z-index: 10000;
        padding: 15px; border-left: 3px solid #00d4ff;
        background: rgba(0, 212, 255, 0.05);
    }}

    /* === THE TYPING AREA FIX (CAPSULE LOOK) === */
    /* Target the container for the entire input */
    .stChatInputContainer {{
        padding: 0 40px !important;
        background-color: transparent !important;
        border: none !important;
        bottom: 50px !important; /* Forces it to float above the bottom edge */
    }}
    
    /* Target the inner text input field */
    .stChatInput {{
        background: rgba(0, 212, 255, 0.05) !important;
        border: 2px solid #00d4ff !important; /* Standard neon blue border */
        border-radius: 50px !important; /* THIS MAKES IT A CAPSULE */
        color: #00d4ff !important;
        padding: 15px 25px !important; /* Internal padding */
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2); /* Slight neon glow */
        font-size: 1.1rem !important;
    }}

    /* Adjust the chat message bubbles to complement the design */
    .stChatMessage {{ 
        background: rgba(0, 212, 255, 0.03) !important; 
        border: 1px solid #00d4ff22 !important; 
        border-radius: 15px !important;
        margin-bottom: 10px;
    }}
    
    </style>
    
    <div class="aegis-hud">
        <h2 style="margin:0; font-size: 1.2rem; letter-spacing: 2px;">AEGIS // MARK I</h2>
        <p style="margin:0; font-size: 0.7rem; color: #00d4ff; opacity: 0.7;">OPERATOR: {USER_NAME.upper()} | STATUS: ONLINE</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. SPEECH & 3D DATA (PERFORMANCE TUNED) ---
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

@st.cache_data # Speed boost from caching the model
def get_aegis_model():
    url = "https://raw.githubusercontent.com/PixelSoldier08/AEGIS-AI/main/download.glb"
    try:
        res = requests.get(url, timeout=10)
        return f"data:application/octet-stream;base64,{base64.b64encode(res.content).decode()}"
    except: return None

model_uri = get_aegis_model()

# --- 4. INTERFACE & 3D RENDER (REPOSITIONED) ---
if model_uri:
    # Repositioned the 3D model slightly higher (bottom: 120px)
    # so it does not collide with the new, floating input capsule.
    st.markdown(f'''
    <div style="position: fixed; bottom: 120px; right: 30px; z-index: 10000;">
        <iframe srcdoc='
            <html>
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <body style="margin:0; background:transparent;">
                <model-viewer src="{model_uri}" auto-rotate rotation-speed="30deg" 
                    camera-controls disable-zoom exposure="1.2"
                    style="width:300px; height:300px; background:transparent; outline:none;">
                </model-viewer>
            </body>
            </html>
        ' style="width:300px; height:300px; border:none;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 5. CHAT ENGINE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Output the historical messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- THE INPUT FIELD ---
if prompt := st.chat_input("Command AEGIS..."):
    # Log and print user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process and print AI response
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are AEGIS. Be concise. Talking to {USER_NAME} in {LOCATION}."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile"
            )
            full_res = response.choices[0].message.content
            st.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            speak(full_res) # Audio feedback
        except Exception as e:
            st.error(f"NEURAL ERROR: {e}")
