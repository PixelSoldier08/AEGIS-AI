import streamlit as st
import psutil
import time
from groq import Groq
from tavily import TavilyClient

# --- 1. BOOT SEQUENCE ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# Initialize Neural and Data Links
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
except Exception as e:
    st.error(f"SYSTEM CRITICAL: Check your Streamlit Secrets. Error: {e}")

# --- 2. HOLOGRAPHIC STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    header, footer, #MainMenu { visibility: hidden; }
    .block-container { padding-top: 150px !important; }

    /* Circular HUD */
    .aegis-header {
        position: fixed; top: 25px; left: 40px; z-index: 9999;
        display: flex; align-items: center; gap: 30px;
    }
    
    /* 3D Zone */
    .projection-zone {
        position: fixed; bottom: 30px; right: 30px; z-index: 1000;
        background: radial-gradient(circle, rgba(0,212,255,0.1) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. COGNITIVE ENGINE ---
def get_aegis_intel(prompt):
    try:
        # Step 1: Live Web Scan
        search = tavily.search(query=prompt, search_depth="advanced")
        context = search['results']
        
        # Step 2: Neural Processing using Llama 3.3
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are AEGIS, a J.A.R.V.I.S.-style AI for Ikki. Location: Tiruchirappalli. Use context: {context}. Respond technically and concisely."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile" # Latest supported model
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Neural Error: {str(e)}"

# --- 4. INTERFACE RENDER ---
def render_ui():
    # HUD Logic
    integrity = int(100 - psutil.cpu_percent())
    offset = 502 - (integrity / 100) * 502
    
    st.markdown(f'''
    <div class="aegis-header">
        <svg width="120" height="120" viewBox="0 0 220 220">
            <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
            <circle stroke="#00d4ff" stroke-width="14" stroke-dasharray="502" 
                    stroke-dashoffset="{offset}" stroke-linecap="round" fill="transparent" r="80" cx="110" cy="110"
                    style="transform: rotate(-90deg); transform-origin: center; filter: drop-shadow(0 0 10px #00d4ff); transition: 1s;"/>
        </svg>
        <div style="border-left: 3px solid #00d4ff; padding-left: 20px;">
            <p style="font-size: 1.6rem; font-weight: bold; margin: 0;">AEGIS // MARK I</p>
            <p style="font-size: 0.75rem; opacity: 0.8;">USER: IKKI | STATUS: ACTIVE</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 3D Spider Projection
    # !! MUST BE THE RAW LINK TO YOUR 3dpea.com_download.glb !!
    model_url = "https://raw.githubusercontent.com/PixelSoldier08/AEGIS-AI/main/3dpea.com_download.glb"
    
    st.markdown('<div class="projection-zone">', unsafe_allow_html=True)
    st.components.v1.html(f"""
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
        <model-viewer src="{model_url}" auto-rotate rotation-speed="40deg" camera-controls disable-zoom 
                      style="width: 250px; height: 250px; background: transparent;"></model-viewer>
    """, height=250)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. EXECUTION LOOP ---
render_ui()

if "history" not in st.session_state: st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if cmd := st.chat_input("Command AEGIS..."):
    st.session_state.history.append({"role": "user", "content": cmd})
    with st.chat_message("user"): st.markdown(cmd)
    
    with st.chat_message("assistant"):
        with st.spinner("SYNAPSING..."):
            ans = get_aegis_intel(cmd)
            st.markdown(ans)
            st.session_state.history.append({"role": "assistant", "content": ans})

# Refresh for HUD animation
time.sleep(2)
st.rerun()
