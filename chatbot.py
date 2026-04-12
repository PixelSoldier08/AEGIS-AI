import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
from tavily import TavilyClient

# --- 1. HUD & STYLING ---
st.set_page_config(page_title="AEGIS: FRIDAY PROTOCOL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #060b14; color: #ff3399; } 
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

# --- 2. INITIALIZE CLIENTS ---
def get_clients():
    try:
        g = Groq(api_key=st.secrets["GROQ_API_KEY"])
        t = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        return g, t
    except Exception as e:
        st.error("Boss, API keys are missing! Add GROQ_API_KEY and TAVILY_API_KEY to Streamlit Secrets.")
        return None, None

client, tavily = get_clients()

# --- 3. THE VOICE PROTOCOL ---
def speak(text):
    clean = text.replace("'", "").replace("\n", " ").replace('"', '')
    st.components.v1.html(f"""
        <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean}');
        function setVoice() {{
            var voices = window.speechSynthesis.getVoices();
            var female = voices.find(v => v.name.includes('Female') || v.name.includes('Hazel') || v.name.includes('Zira') || v.name.includes('Google UK English Female'));
            if (female) msg.voice = female;
            msg.rate = 1.1; msg.pitch = 1.2;
            window.speechSynthesis.speak(msg);
        }}
        if (window.speechSynthesis.getVoices().length !== 0) {{ setVoice(); }}
        else {{ window.speechSynthesis.onvoiceschanged = setVoice; }}
        </script>
    """, height=0)

# --- 4. BOOT SEQUENCE ---
if 'booted' not in st.session_state:
    intro = st.empty()
    with intro.container():
        # High-tech HUD animation
        res = requests.get("https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json")
        lottie_json = res.json() if res.status_code == 200 else None
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if lottie_json:
                st_lottie(lottie_json, height=400, key="boot_lottie")
            bar = st.progress(0)
            msg_status = st.empty()
            steps = ["UPLOADING FRIDAY OS...", "CALIBRATING NEURAL LINKS...", "FRIDAY ONLINE."]
            for i, s in enumerate(steps):
                msg_status.markdown(f"`{s}`")
                bar.progress((i + 1) * 33)
                time.sleep(0.7)
            speak("Welcome back, Boss. All systems green.")
    st.session_state.booted = True
    intro.empty()

# --- 5. THE CHAT SECTION ---
if st.session_state.get('booted'):
    st.title("AEGIS: FRIDAY PROTOCOL")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input section
    if prompt := st.chat_input("Command FRIDAY..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                # A. Search
                context = ""
                try:
                    search = tavily.search(query=prompt)
                    context = str(search['results'])
                except:
                    context = "No live data."

                # B. Brain (Using Llama 3.1)
                try:
                    chat_completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": f"You are FRIDAY. Be sharp and efficient. Call the user Boss. Context: {context}"},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    response = chat_completion.choices[0].message.content
                except Exception as e:
                    response = f"Boss, my neural links are unstable. Error: {e}"
                
                st.markdown(response)
                speak(response)
                
        st.session_state.messages.append({"role": "assistant", "content": response})
