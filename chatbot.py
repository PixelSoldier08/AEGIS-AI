import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
from tavily import TavilyClient

# --- 1. HUD & INTERFACE CONFIG ---
st.set_page_config(page_title="AEGIS: FRIDAY PROTOCOL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #060b14; color: #ff3399; } /* Subtle pink/magenta accent for FRIDAY */
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

# --- 2. BRAIN INITIALIZATION ---
def get_globals():
    try:
        # Pulling keys from Streamlit Secrets
        g_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        t_client = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        return g_client, t_client
    except Exception as e:
        st.error(f"Configuration Error: {e}")
        return None, None

client, tavily = get_globals()

# --- 3. FRIDAY VOICE UTILITY ---
def speak(text):
    """Web-based female voice (FRIDAY)"""
    clean = text.replace("'", "").replace("\n", " ").replace('"', '')
    st.components.v1.html(f"""
        <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean}');
        var voices = window.speechSynthesis.getVoices();
        
        // Try to find a female-sounding voice
        msg.voice = voices.find(v => v.name.includes('Female') || v.name.includes('Google UK English Female') || v.name.includes('Hazel'));
        
        msg.rate = 1.1; // FRIDAY talks a bit faster/sharper
        msg.pitch = 1.2; // Slightly higher pitch for female tone
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 4. UTILITIES ---
def load_lottie(url):
    try:
        res = requests.get(url, timeout=5)
        return res.json() if res.status_code == 200 else None
    except: return None

# --- 5. BOOT SEQUENCE ---
if 'booted' not in st.session_state:
    intro = st.empty()
    with intro.container():
        # High-tech HUD animation
        lottie_json = load_lottie("https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if lottie_json: st_lottie(lottie_json, height=400, key="boot")
            bar = st.progress(0)
            msg = st.empty()
            steps = ["UPLOADING FRIDAY OS...", "CALIBRATING NEURAL LINKS...", "FRIDAY ONLINE."]
            for i, s in enumerate(steps):
                msg.markdown(f"`{s}`")
                bar.progress((i + 1) * 33)
                time.sleep(0.8)
            speak("Boss? You're up? All systems operational.")
    st.session_state.booted = True
    intro.empty()

# --- 6. CHAT INTERFACE & REASONING ---
if st.session_state.get('booted') and client:
    st.title("AEGIS: FRIDAY PROTOCOL")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Command FRIDAY..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Scanning Data..."):
                # A. Web Search (Tavily)
                context = ""
                try:
                    search = tavily.search(query=prompt)
                    context = str(search['results'])
                except: context = "No live satellite data."

                # B. Brain (Llama 3.1)
                try:
                    chat_completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": f"You are FRIDAY, the female AI from Iron Man. Be efficient and call the user Boss. Use this data: {context}"},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    response = chat_completion.choices[0].message.content
                except:
                    response = "Neural link dropped, Boss. Check your API connections."
                
                st.markdown(response)
                speak(response) # Friday speaks the response
                
        st.session_state.messages.append({"role": "assistant", "content": response})
