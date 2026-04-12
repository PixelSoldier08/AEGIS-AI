import streamlit as st
import time
import requests
import pyttsx3
import threading
from streamlit_lottie import st_lottie

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="AEGIS OS", page_icon="🌐", layout="wide")

# Custom CSS for the "Jarvis" Glow Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #060b14; color: #00f2ff; }
    .stMarkdown, p, h1, h2, h3 { 
        color: #00f2ff !important; 
        text-shadow: 0 0 5px #00f2ff;
        font-family: 'Courier New', monospace;
    }
    /* Glassmorphism for chat bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def speak(text):
    """Runs TTS in a separate thread to prevent Streamlit UI freezing"""
    def run_speech():
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id) # Usually male/British-sounding
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speech).start()

# --- 3. THE BOOT SEQUENCE (INTRO) ---
if 'booted' not in st.session_state:
    intro_placeholder = st.empty()
    
    with intro_placeholder.container():
        # Load a techy HUD animation (Replace URL with your favorite)
        lottie_url = "https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json"
        lottie_json = load_lottieurl(lottie_url)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(lottie_json, height=450, key="boot_anim")
            
            status = st.empty()
            bar = st.progress(0)
            
            boot_logs = [
                "INITIALIZING AEGIS CORE...",
                "LOADING NEURAL NETWORKS...",
                "SYNCING STARK-HUD INTERFACE...",
                "BYPASSING SECURITY PROTOCOLS...",
                "AEGIS ONLINE."
            ]
            
            for i, log in enumerate(boot_logs):
                status.markdown(f"`{log}`")
                bar.progress((i + 1) * 20)
                time.sleep(0.7)
            
            speak("Welcome home, sir. AEGIS is at your service.")
            time.sleep(1.5)
            
    st.session_state.booted = True
    intro_placeholder.empty() # Clears the screen for the main app

# --- 4. MAIN CHATBOT INTERFACE ---
if st.session_state.get('booted'):
    st.title("AEGIS v2.0")
    
    # Persistent sidebar animation
    with st.sidebar:
        st.markdown("### Core Status: Active")
        lottie_sidebar = load_lottieurl("https://lottie.host/9f50e64c-f17b-4b10-9946-815340626372/pM7vA8n48H.json")
        st_lottie(lottie_sidebar, height=150, key="sidebar_anim")
        st.divider()
        st.info("Ask me about system status or current web trends.")

    # Chat history logic from your existing script
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
            # Put your actual AI generation (Groq/Tavily) logic here
            response = "I am processing your request using the Aegis interface." 
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
