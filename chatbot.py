import streamlit as st
import psutil
import time

# --- INITIAL CONFIG ---
st.set_page_config(page_title="AEGIS HUD", layout="wide", initial_sidebar_state="collapsed")

# --- STARK INDUSTRIES STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    /* Background & Main Font */
    .stApp {
        background-color: #060b10;
        color: #00d4ff;
        font-family: 'Orbitron', sans-serif;
    }

    /* Hide Streamlit Branding */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Floating HUD Container */
    .floating-hud {
        position: fixed;
        top: 30px;
        left: 30px;
        z-index: 1000;
        pointer-events: none;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* SVG Animation */
    .ring-circle {
        transition: stroke-dashoffset 0.8s ease-in-out;
        transform: rotate(-90deg);
        transform-origin: center;
        filter: drop-shadow(0 0 12px #00d4ff);
    }

    /* HUD Text Styling */
    .hud-label {
        position: absolute;
        top: 85px;
        text-align: center;
        width: 100%;
    }

    .percent-val { font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 10px #00d4ff; }
    .sub-label { font-size: 0.5rem; letter-spacing: 2px; opacity: 0.8; }

    /* Custom Scrollbar for that Tech Look */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #060b10; }
    ::-webkit-scrollbar-thumb { background: #1a3a4a; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- HUD LOGIC ---
def render_floating_hud():
    # Calculate System Health (100 - CPU Usage)
    cpu = psutil.cpu_percent()
    health = 100 - cpu
    
    # SVG Constants (Circumference for R=80 is ~502)
    circum = 502
    offset = circum - (health / 100) * circum
    
    # Alert Color Logic
    color = "#ff4b2b" if health < 30 else "#00d4ff"
    
    hud_html = f"""
    <div class="floating-hud">
        <svg width="220" height="220">
            <circle stroke="#1a3a4a" stroke-width="4" fill="transparent" r="80" cx="110" cy="110"/>
            <circle class="ring-circle" stroke="{color}" stroke-width="10" 
                    stroke-dasharray="{circum}" stroke-dashoffset="{offset}" 
                    stroke-linecap="round" fill="transparent" r="80" cx="110" cy="110"
                    style="filter: drop-shadow(0 0 8px {color});"/>
        </svg>
        <div class="hud-label">
            <div class="percent-val" style="color: {color};">{int(health)}%</div>
            <div class="sub-label" style="color: {color};">SYS_INTEGRITY</div>
        </div>
    </div>
    """
    st.markdown(hud_html, unsafe_allow_html=True)

# --- INTERFACE LAYOUT ---
render_floating_hud()

st.write(f"### AEGIS // NEURAL INTERFACE")
st.write(f"**USER:** IKKI | **LOC:** TIRUCHIRAPPALLI")
st.write("---")

# Chat Container
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Command AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simulated Response Logic
    with st.chat_message("assistant"):
        response = f"Processing '{prompt}'... Terminal link established."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# This forces the page to refresh and update the CPU health bar every 2 seconds
time.sleep(2)
st.rerun()
