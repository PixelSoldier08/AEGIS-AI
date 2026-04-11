import streamlit as st
import psutil
import time

# --- CONFIG ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide", initial_sidebar_state="collapsed")

# --- CSS BLOCK ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    .block-container { padding-top: 150px !important; }
    header, footer, #MainMenu {visibility: hidden;}

    /* The Main Floating HUD Container */
    .aegis-header-container {
        position: fixed;
        top: 20px;
        left: 30px;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 25px;
        pointer-events: none;
    }

    .aegis-info-block {
        border-left: 3px solid #00d4ff;
        padding-left: 20px;
        display: flex;
        flex-direction: column;
    }

    .title-text { font-size: 1.5rem; font-weight: bold; letter-spacing: 2px; text-shadow: 0 0 10px #00d4ff; margin: 0; }
    .sub-text { font-size: 0.7rem; letter-spacing: 1px; opacity: 0.8; margin: 5px 0 0 0; }
    
    .ring-circle { transition: stroke-dashoffset 0.8s ease; transform: rotate(-90deg); transform-origin: center; }
    </style>
""", unsafe_allow_html=True)

# --- HUD GENERATOR ---
def render_aegis_hud():
    integrity = 100 - psutil.cpu_percent()
    circum = 502
    offset = circum - (integrity / 100) * circum
    color = "#ff4b2b" if integrity < 30 else "#00d4ff"
    
    # We use a f-string here. Ensure no accidental backslashes or quotes break it.
    hud_html = f"""
    <div class="aegis-header-container">
        <div style="position: relative; width: 120px; height: 120px;">
            <svg width="120" height="120" viewBox="0 0 220 220">
                <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
                <circle class="ring-circle" stroke="{color}" stroke-width="12" 
                        stroke-dasharray="{circum}" stroke-dashoffset="{offset}" 
                        stroke-linecap="round" fill="transparent" r="80" cx="110" cy="110"
                        style="filter: drop-shadow(0 0 8px {color});"/>
            </svg>
            <div style="position: absolute; top: 40px; left: 0; width: 100%; text-align: center;">
                <div style="color: {color}; font-size: 1.2rem; font-weight: bold;">{int(integrity)}%</div>
                <div style="color: {color}; font-size: 0.4rem; letter-spacing: 1px;">INTEGRITY</div>
            </div>
        </div>
        <div class="aegis-info-block">
            <p class="title-text">AEGIS // NEURAL INTERFACE</p>
            <p class="sub-text">USER: IKKI | LOC: TIRUCHIRAPPALLI | STATUS: ACTIVE</p>
        </div>
    </div>
    """
    # CRITICAL: This line must have unsafe_allow_html=True
    st.markdown(hud_html, unsafe_allow_html=True)

# --- EXECUTION ---
render_aegis_hud()

# Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = f"Acknowledged. Analysis of '{prompt}' is in progress."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Refresh rate
time.sleep(2)
st.rerun()
