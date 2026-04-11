import streamlit as st
import psutil
import time
from groq import Groq
from streamlit_obj_3d_viewer import obj_3d_viewer

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# Styling: High-Tech Stark Aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    .block-container { padding-top: 180px !important; }
    header, footer, #MainMenu { visibility: hidden; }

    .aegis-header {
        position: fixed; top: 25px; left: 40px; z-index: 9999;
        display: flex; align-items: center; gap: 25px; pointer-events: none;
    }
    .aegis-info { border-left: 3px solid #00d4ff; padding-left: 20px; }
    .title-text { font-size: 1.6rem; font-weight: bold; text-shadow: 0 0 10px #00d4ff; margin: 0; }
    .sub-text { font-size: 0.75rem; opacity: 0.8; margin-top: 5px; letter-spacing: 1px; }
    
    .floating-3d { position: fixed; bottom: 40px; right: 40px; z-index: 1000; pointer-events: auto; }
    </style>
""", unsafe_allow_html=True)

# --- NEURAL LINK (GROQ) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_intel(prompt):
    try:
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are AEGIS, a Stark-inspired AI for Ikki in Tiruchirappalli. You are an expert in Physics and Python simulations. Be technical, helpful, and concise."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Neural Error: {str(e)}"

# --- VOICE CORE ---
def speak(text):
    clean_text = text.replace("'", "\\'")
    st.components.v1.html(f"""
        <script>
        var s = window.speechSynthesis;
        var u = new SpeechSynthesisUtterance('{clean_text}');
        u.pitch = 0.85; u.rate = 1.1;
        s.speak(u);
        </script>
    """, height=0)

# --- INTERFACE RENDER ---
integrity = int(100 - psutil.cpu_percent())
offset = 502 - (integrity / 100) * 502

st.markdown(f'''
<div class="aegis-header">
    <svg width="120" height="120" viewBox="0 0 220 220">
        <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
        <circle stroke="#00d4ff" stroke-width="12" stroke-dasharray="502" stroke-dashoffset="{offset}" 
                fill="transparent" r="80" cx="110" cy="110" style="transform: rotate(-90deg); transform-origin: center; transition: 1s;"/>
    </svg>
    <div class="aegis-info">
        <p class="title-text">AEGIS // MARK I</p>
        <p class="sub-text">USER: IKKI | STATUS: ONLINE | CORE: {integrity}%</p>
    </div>
</div>
''', unsafe_allow_html=True)

# 3D Spider-Logo Projection Zone
with st.container():
    st.markdown('<div class="floating-3d">', unsafe_allow_html=True)
    # Replace URL with your actual Spider-Man .obj file link
    obj_3d_viewer("https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF/Duck.gltf")
    st.markdown('</div>', unsafe_allow_html=True)

# --- CHAT ENGINE ---
if "history" not in st.session_state: st.session_state.history = []

for m in st.session_state.history:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if p := st.chat_input("Command AEGIS..."):
    st.session_state.history.append({"role": "user", "content": p})
    with st.chat_message("user"): st.markdown(p)
    with st.chat_message("assistant"):
        response = get_intel(p)
        st.markdown(response)
        speak(response)
        st.session_state.history.append({"role": "assistant", "content": response})

time.sleep(2)
st.rerun()
