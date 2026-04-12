import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
from tavily import TavilyClient

# --- CONFIGURATION ---
st.set_page_config(page_title="AEGIS OS", page_icon="🌐", layout="wide")

# CSS for the HUD Glow
st.markdown("""
    <style>
    .stApp { background-color: #060b14; color: #00f2ff; }
    .stMarkdown, p, h1, h2, h3 { 
        color: #00f2ff !important; 
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.6);
        font-family: 'Courier New', monospace;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def speak_web(text):
    """Voice that works on the Web/Cloud"""
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text}');
        msg.rate = 1.0; 
        msg.pitch = 0.8;
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- BOOT SEQUENCE ---
if 'booted' not in st.session_state:
    intro_placeholder = st.empty()
    
    with intro_placeholder.container():
        # Reliable Lottie URL for AI Circle
        lottie_url = "https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json"
        lottie_json = load_lottieurl(lottie_url)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # ONLY show if JSON loaded correctly to avoid the APIException
            if lottie_json:
                st_lottie(lottie_json, height=400, key="boot_anim")
            else:
                st.subheader("SYSTEM LOADING...")
            
            status = st.empty()
            bar = st.progress(0)
            
            steps = ["INITIALIZING AEGIS...", "ESTABLISHING LINKS...", "SYSTEMS ONLINE."]
            for i, step in enumerate(steps):
                status.markdown(f"**{step}**")
                bar.progress((i + 1) * 33)
                time.sleep(1.0)
            
            speak_web("Welcome home, sir.")
            time.sleep(1)
            
    st.session_state.booted = True
    intro_placeholder.empty()

# --- MAIN CHATBOT LOGIC ---
if st.session_state.get('booted'):
    st.title("AEGIS v2.0")
    
    # Simple Chat logic placeholder (Insert your Groq logic here)
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
            response = "Command acknowledged. Processing data streams."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
