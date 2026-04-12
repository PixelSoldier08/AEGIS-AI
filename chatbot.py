import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
from tavily import TavilyClient

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="AEGIS OS", page_icon="🌐", layout="wide")

# Custom CSS for the Stark/HUD Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #060b14; color: #00f2ff; }
    .stMarkdown, p, h1, h2, h3 { 
        color: #00f2ff !important; 
        text-shadow: 0 0 8px rgba(0, 242, 255, 0.6);
        font-family: 'Courier New', monospace;
    }
    /* Chat Bubble Styling */
    [data-testid="stChatMessage"] {
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE CLIENTS (Add your keys here) ---
# It's better to use st.secrets["GROQ_API_KEY"] if deploying to Streamlit Cloud
GROQ_API_KEY = "YOUR_GROQ_KEY_HERE"
TAVILY_API_KEY = "YOUR_TAVILY_KEY_HERE"

client = Groq(api_key=GROQ_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# --- HELPER FUNCTIONS ---
def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def speak_web(text):
    """Browser-based TTS that works everywhere"""
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text}');
        msg.rate = 1.0; 
        msg.pitch = 0.8; // Lower pitch for a more 'AI' feel
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- BOOT SEQUENCE (Intro Animation) ---
if 'booted' not in st.session_state:
    intro_placeholder = st.empty()
    
    with intro_placeholder.container():
        # Using a sleek circular tech animation
        lottie_url = "https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json"
        lottie_json = load_lottieurl(lottie_url)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(lottie_json, height=400, key="boot_anim")
            
            status = st.empty()
            bar = st.progress(0)
            
            steps = ["INITIALIZING CORE...", "SYNCING HUD...", "AEGIS ONLINE."]
            for i, step in enumerate(steps):
                status.markdown(f"**{step}**")
                bar.progress((i + 1) * 33)
                time.sleep(0.8)
            
            speak_web("Welcome home, sir. All systems are operational.")
            time.sleep(1)
            
    st.session_state.booted = True
    intro_placeholder.empty()

# --- MAIN INTERFACE ---
if st.session_state.get('booted'):
    # Sidebar HUD Elements
    with st.sidebar:
        st.title("AEGIS v2.0")
        sidebar_anim = load_lottieurl("https://lottie.host/9f50e64c-f17b-4b10-9946-815340626372/pM7vA8n48H.json")
        st_lottie(sidebar_anim, height=150)
        st.write("---")
        st.write("System Status: **OPTIMAL**")
        if st.button("Reboot System"):
            del st.session_state.booted
            st.rerun()

    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Command
    if prompt := st.chat_input("Input Command..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Processing
        with st.chat_message("assistant"):
            with st.spinner("Analyzing Data..."):
                # 1. Search the web using Tavily
                search_result = tavily.search(query=prompt, search_depth="basic")
                context = str(search_result['results'])

                # 2. Generate response using Groq
                completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": f"You are AEGIS, a sophisticated AI. Use this context: {context}"},
                        {"role": "user", "content": prompt}
                    ]
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                
        st.session_state.messages.append({"role": "assistant", "content": response})
