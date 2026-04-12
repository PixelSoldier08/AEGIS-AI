import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
from tavily import TavilyClient

# --- 1. HUD DESIGN & PAGE CONFIG ---
st.set_page_config(page_title="AEGIS OS", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #060b14; color: #00f2ff; }
    .stMarkdown, p, h1, h2, h3 { 
        color: #00f2ff !important; 
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.7);
        font-family: 'Courier New', monospace;
    }
    [data-testid="stChatMessage"] {
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. CONNECTING THE BRAINS ---
# Replace these with your actual keys
GROQ_KEY = "YOUR_GROQ_API_KEY"
TAVILY_KEY = "YOUR_TAVILY_API_KEY"

client = Groq(api_key=GROQ_KEY)
tavily = TavilyClient(api_key=TAVILY_KEY)

# --- 3. CORE UTILITIES (Voice & Animation) ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def speak_web(text):
    """Voice that works on the Web/Cloud"""
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text.replace("'", "")}');
        msg.rate = 1.0; msg.pitch = 0.8;
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 4. THE JARVIS BOOT SEQUENCE ---
if 'booted' not in st.session_state:
    intro = st.empty()
    with intro.container():
        # High-tech HUD animation
        lottie_json = load_lottieurl("https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if lottie_json:
                st_lottie(lottie_json, height=400, key="boot")
            bar = st.progress(0)
            status = st.empty()
            for i, s in enumerate(["INITIALIZING AEGIS...", "SYNCING NEURAL NETS...", "SYSTEMS ONLINE."]):
                status.markdown(f"`{s}`")
                bar.progress((i + 1) * 33)
                time.sleep(1.0)
            speak_web("Welcome home, sir. AEGIS is operational.")
    st.session_state.booted = True
    intro.empty()

# --- 5. CHAT INTERFACE & LIVE REASONING ---
if st.session_state.get('booted'):
    st.title("AEGIS v2.0")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Command AEGIS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing Data Streams..."):
                # A. Web Search (The Calculation)
                try:
                    search = tavily.search(query=prompt, search_depth="basic")
                    context = str(search['results'])
                except:
                    context = "No live data found."

                # B. AI Reasoning (The Brain)
                chat_completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": f"You are AEGIS, a highly advanced AI. Use this live data: {context}"},
                        {"role": "user", "content": prompt}
                    ]
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                # speak_web(response) # Uncomment if you want him to speak every reply
                
        st.session_state.messages.append({"role": "assistant", "content": response})
