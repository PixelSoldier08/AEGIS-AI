import streamlit as st
import psutil
import requests
import base64
from groq import Groq

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="AEGIS MARK I", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Identity Lock
USER_NAME = "Ikki"
LOCATION = "Tiruchirappalli"

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"NEURAL LINK ERROR: {e}")

# --- 2. THE TOTAL INTERFACE OVERRIDE (MOTION + CAPSULE + NO GAP) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    /* ANIMATED MOTION BACKGROUND */
    .stApp {{
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%) !important;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
        overflow: hidden !important;
    }}

    /* Parallax Starfield */
    @keyframes moveStars {{
        from {{ transform: translateY(0px); }}
        to {{ transform: translateY(-2000px); }}
    }}
    .stars {{
        position: fixed; top: 0; left: 0; width: 100%; height: 2000px;
        background: transparent url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        z-index: -1;
        animation: moveStars 120s linear infinite;
        opacity: 0.3;
    }}

    /* REMOVE ALL BLANK SPACE AT BOTTOM */
    .main .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
        max-width: 95% !important;
    }}
    footer {{display: none !important; visibility: hidden !important;}}
    [data-testid="stHeader"] {{display: none !important;}}

    /* === DUAL-LAYER HUD RING === */
    .aegis-hud-container {{
        position: fixed; top: 25px; left: 40px; z-index: 10000;
        display: flex; align-items: center; gap: 20px;
    }}
    .hud-ring-outer {{
        width: 70px; height: 70px;
        border: 2px dashed #00d4ff;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        animation: spin-slow 10s linear infinite;
    }}
    .hud-ring-inner {{
        width: 45px; height: 45px;
        border: 3px solid #00d4ff;
        border-top: 3px solid transparent;
        border-radius: 50%;
        animation: spin-fast 2s linear infinite;
    }}
    @keyframes spin-slow {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    @keyframes spin-fast {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

    /* === THE CAPSULE FIX (VERSION FINAL) === */
    div[data-testid="stChatInput"] {{
        background-color: transparent !important;
        border: none !important;
        position: fixed !important;
        bottom: 25px !important; /* Fixed at the very bottom */
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 600px !important;
        padding: 0 !important;
        z-index: 10001 !important;
    }}

    div[data-testid="stChatInput"] > div {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    div[data-testid="stChatInput"] textarea {{
        background: rgba(0, 212, 255, 0.08) !important;
        border: 2px solid #00d4ff !important;
        border-radius: 100px !important; 
        color: #00d4ff !important;
        padding: 12px 60px 12px 25px !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2) !important;
        line-height: 1.6 !important;
        height: 55px !important;
    }}

    div[data-testid="stChatInput"] button {{
        background-color: transparent !important;
        color: #00d4ff !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        right: 15px !important
