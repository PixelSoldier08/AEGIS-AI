import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
from tavily import TavilyClient
import openai # Added this back
import tools  # Importing your local tools.py

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
        o = None
        if "OPENAI_API_KEY" in st.secrets:
            o = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        return g, t, o
    except Exception as e:
        st.error(f"Boss, API keys are missing! {e}")
        return None, None, None

client, tavily, openai_client = get_clients()

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

# --- 4. IMAGE GENERATION ---
def draw_image(prompt):
    if not openai_client:
        return "ERROR: Visualizer key not found."
    try:
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=f"Cinematic Marvel style: {prompt}",
            n=1, size="1024x1024"
        )
        return response.data[0].url
    except Exception as e:
        return f"ERROR: {e}"

# --- 5. BOOT SEQUENCE ---
if 'booted' not in st.session_state:
    intro = st.empty()
    with intro.container():
        res = requests.get("https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json")
        lottie_json = res.json() if res.status_code == 200 else None
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if lottie_json: st_lottie(lottie_json, height=400, key="boot")
            bar = st.progress(0)
            for i, s in enumerate(["LOADING FRIDAY...", "SYNCING BRAIN...", "READY."]):
                st.markdown(f"`{s}`")
                bar.progress((i + 1) * 33)
                time.sleep(0.6)
            speak("Welcome back, Boss.")
    st.session_state.booted = True
    intro.empty()

# --- 6. CHAT SECTION ---
if st.session_state.get('booted'):
    st.title("AEGIS: FRIDAY PROTOCOL")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if m["type"] == "text": st.markdown(m["content"])
            else: st.image(m["content"])

    if prompt := st.chat_input("Command FRIDAY..."):
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # Check if user wants to draw
            if any(k in prompt.lower() for k in ["draw", "visualize", "show me"]):
                with st.spinner("Visualizing..."):
                    img_result = draw_image(prompt)
                    if "ERROR" in img_result:
                        st.markdown("Visualizer offline, Boss. (Check OpenAI Key)")
                    else:
                        st.image(img_result)
                        st.session_state.messages.append({"role": "assistant", "type": "image", "content": img_result})
                        speak("Here is the visualization.")
            else:
                # Normal Chat
                with st.spinner("Analyzing..."):
                    search_context = tools.web_search(prompt) # Using your tools.py
                    ans = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "system", "content": f"You are FRIDAY. Use this: {search_context}"}, {"role": "user", "content": prompt}]
                    ).choices[0].message.content
                    st.markdown(ans)
                    speak(ans)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": ans})
