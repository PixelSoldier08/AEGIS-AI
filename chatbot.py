import streamlit as st
import psutil
import time

# --- STYLING (Integrating the Stark Look) ---
st.set_page_config(page_title="AEGIS MARK I", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #060b10; color: #00d4ff; font-family: 'Orbitron', sans-serif; }
    
    /* Glowing Circular HUD */
    .hud-container {
        display: flex; justify-content: center; align-items: center; position: relative; height: 250px;
    }
    .ring-circle {
        transition: stroke-dashoffset 0.5s ease;
        transform: rotate(-90deg); transform-origin: 50% 50%;
        filter: drop-shadow(0 0 10px #00d4ff);
    }
    .hud-text { position: absolute; text-align: center; }
    .percent { font-size: 2rem; font-weight: bold; text-shadow: 0 0 10px #00d4ff; }
    </style>
""", unsafe_allow_html=True)

# --- HUD COMPONENT FUNCTION ---
def render_hud():
    # Drive the health bar using real System Integrity (100 - CPU Usage)
    health = 100 - psutil.cpu_percent()
    offset = 502 - (health / 100) * 502
    color = "#ff4b2b" if health < 30 else "#00d4ff"
    
    hud_html = f"""
    <div class="hud-container">
        <svg width="220" height="220">
            <circle stroke="#1a3a4a" stroke-width="5" fill="transparent" r="80" cx="110" cy="110"/>
            <circle class="ring-circle" stroke="{color}" stroke-width="10" 
                    stroke-dasharray="502" stroke-dashoffset="{offset}" 
                    fill="transparent" r="80" cx="110" cy="110"/>
        </svg>
        <div class="hud-text">
            <div class="percent" style="color: {color};">{int(health)}%</div>
            <div style="font-size: 0.6rem; letter-spacing: 2px;">SYS_INTEGRITY</div>
        </div>
    </div>
    """
    st.sidebar.markdown(hud_html, unsafe_allow_html=True)

# --- MAIN INTERFACE ---
st.title("AEGIS // NEURAL INTERFACE")

# Sidebar for System Stats (HUD)
with st.sidebar:
    st.header("CORE STATUS")
    render_hud()
    st.write("---")
    st.write(f"Location: Tiruchirappalli")
    st.write(f"User: Ikki")

# Chat Interface Logic (From our shared link)
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
        response = f"System analysis of '{prompt}' complete. Standing by for execution."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Refresh trigger to keep the HUD moving
time.sleep(0.1)
st.rerun()
