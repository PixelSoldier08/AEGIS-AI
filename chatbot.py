import streamlit as st
import psutil
import time
from groq import Groq
from tavily import TavilyClient

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# Connect to Neural Networks
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. HOLOGRAPHIC INTERFACE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container { padding-top: 150px !important; }

    .aegis-header {
        position: fixed; top: 25px; left: 40px; z-index: 9999;
        display: flex; align-items: center; gap: 20px;
    }
    .projection-zone {
        position: fixed; bottom: 30px; right: 30px; z-index: 9999;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CORE ENGINES ---
def speak(text):
    if text:
        clean_text = text.replace("'", "\\'").replace("\n", " ")
        st.components.v1.html(f"""
            <script>
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance('{clean_text}');
            u.pitch = 0.85; u.rate = 1.05; 
            window.speechSynthesis.speak(u);
            </script>
        """, height=0)

def get_aegis_intel(prompt):
    try:
        search = tavily.search(query=prompt, search_depth="advanced")
        context = search['results']
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are AEGIS for Ikki. Tiruchirappalli context: {context}. Be professional."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Neural Error: {str(e)}"

# --- 4. INTERFACE RENDER ---
def render_ui():
    # HUD Alignment
    integrity = int(100 - psutil.cpu_percent())
    offset = 502 - (integrity / 100) * 502
    
    st.markdown(f'''
    <div class="aegis-header">
        <svg width="100" height="100" viewBox="0 0 220 220">
            <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
            <circle stroke="#00d4ff" stroke-width="12" stroke-dasharray="502" 
                    stroke-dashoffset="{offset}" stroke-linecap="round" fill="transparent" r="80" cx="110" cy="110"
                    style="transform: rotate(-90deg); transform-origin: center; filter: drop-shadow(0 0 8px #00d4ff); transition: 1.5s;"/>
        </svg>
        <div style="border-left: 2px solid #00d4ff; padding-left: 15px;">
            <p style="font-size: 1.5rem; font-weight: bold; margin: 0;">AEGIS // MARK I</p>
            <p style="font-size: 0.7rem; opacity: 0.8;">USER: IKKI | LOC: TIRUCHIRAPPALLI</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 3D Hologram - Using the new 'download.glb' file
    model_url = "https://github.com/PixelSoldier08/AEGIS-AI/blob/main/download.glb?raw=true"
    
    st.markdown(f'''
    <div class="projection-zone">
        <iframe srcdoc='
            <html>
            <head>
                <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            </head>
            <body style="margin: 0; background: transparent; overflow: hidden;">
                <model-viewer src="{model_url}" auto-rotate rotation-speed="40deg" 
                    camera-controls disable-zoom style="width: 300px; height: 300px; background: transparent; outline: none;">
                </model-viewer>
            </body>
            </html>
        ' style="width: 300px; height: 300px; border: none; background: transparent;"></iframe>
    </div>
    ''', unsafe_allow_html=True)

# --- 5. LOGIC LOOP ---
render_ui()

if "history" not in st.session_state: st.session_state.history = []
if "last_ans" not in st.session_state: st.session_state.last_ans = None

for m in st.session_state.history:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if cmd := st.chat_input("Command AEGIS..."):
    st.session_state.history.append({"role": "user", "content": cmd})
    with st.chat_message("user"): st.markdown(cmd)
    
    with st.chat_message("assistant"):
        ans = get_aegis_intel(cmd)
        st.markdown(ans)
        st.session_state.history.append({"role": "assistant", "content": ans})
        st.session_state.last_ans = ans
        st.rerun()

if st.session_state.last_ans:
    speak(st.session_state.last_ans)
    st.session_state.last_ans = None

time.sleep(3)
st.rerun()
