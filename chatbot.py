import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
import openai
import tools # Ensure tools.py is in your GitHub repo

# --- 1. HUD & STYLING (The Glowing Interface) ---
st.set_page_config(page_title="AEGIS: FRIDAY PROTOCOL", layout="wide")

st.markdown("""
    <style>
    /* Dark Sci-Fi Background */
    .stApp { 
        background-color: #060b14; 
    }
    
    /* Glowing Neon Cyan for Headers and Text */
    .stMarkdown, p, h1, h2, h3, li { 
        color: #00f2ff !important; 
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.7), 0 0 5px rgba(0, 242, 255, 0.4);
        font-family: 'Courier New', monospace;
    }

    /* Pink Accents for specific UI elements */
    .stChatInputContainer {
        border-top: 1px solid #ff3399 !important;
    }

    /* Custom Chat Bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(0, 242, 255, 0.05) !important;
        border: 1px solid rgba(0, 242, 255, 0.2) !important;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZE CLIENTS ---
def get_clients():
    try:
        g = Groq(api_key=st.secrets["GROQ_API_KEY"])
        # OpenAI is optional if trial expires
        o = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) if "OPENAI_API_KEY" in st.secrets else None
        return g, o
    except Exception as e:
        st.error(f"Satellite link failed: {e}")
        return None, None

client, openai_client = get_clients()

# --- 3. VOICE PROTOCOL (Clean & Tab-Aware) ---
def speak(text):
    # Sanitize text to prevent noise/static
    clean = text.replace("'", "").replace('"', "").replace("\n", " ").replace("*", "")
    st.components.v1.html(f"""
        <script>
        // Stop current speech before starting new
        window.speechSynthesis.cancel(); 
        
        // Stop speech immediately if user switches tabs
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{ window.speechSynthesis.cancel(); }}
        }});

        setTimeout(() => {{
            var msg = new SpeechSynthesisUtterance('{clean}');
            var voices = window.speechSynthesis.getVoices();
            // Force Female/Hazel voice selection
            var female = voices.find(v => v.name.includes('Female') || v.name.includes('Hazel') || v.name.includes('Google UK English Female'));
            if (female) msg.voice = female;
            msg.rate = 1.05; msg.pitch = 1.2;
            window.speechSynthesis.speak(msg);
        }}, 100);
        </script>
    """, height=0)

# --- 4. BOOT SEQUENCE ---
if 'booted' not in st.session_state:
    boot_placeholder = st.empty()
    with boot_placeholder.container():
        res = requests.get("https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json")
        lottie_json = res.json() if res.status_code == 200 else None
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if lottie_json: st_lottie(lottie_json, height=350, key="boot")
            bar = st.progress(0)
            status = st.empty()
            
            load_steps = [
                ("UPLOADING FRIDAY OS...", 33),
                ("CALIBRATING HUD...", 66),
                ("SYSTEMS GREEN.", 100)
            ]
            for s, v in load_steps:
                status.markdown(f"**`{s}`**")
                bar.progress(v)
                time.sleep(0.7)
            
            speak("Welcome back, Boss. All systems operational.")
    st.session_state.booted = True
    boot_placeholder.empty()

# --- 5. CHAT ENGINE ---
if st.session_state.get('booted'):
    st.title("AEGIS: FRIDAY PROTOCOL")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if m["type"] == "text": st.markdown(m["content"])
            else: st.image(m["content"])

    if prompt := st.chat_input("Command FRIDAY..."):
        # Kill speech on new command
        st.components.v1.html("<script>window.speechSynthesis.cancel();</script>", height=0)
        
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # A. VISUALIZATION REQUEST
            if any(k in prompt.lower() for k in ["draw", "visualize", "image", "picture"]):
                if openai_client:
                    with st.spinner("Accessing visual sub-routines..."):
                        try:
                            res = openai_client.images.generate(
                                model="dall-e-3", 
                                prompt=f"Cinematic Marvel style, high tech HUD: {prompt}",
                                n=1
                            )
                            url = res.data[0].url
                            st.image(url)
                            st.session_state.messages.append({"role": "assistant", "type": "image", "content": url})
                            speak("The visualization is on your screen, Boss.")
                        except:
                            st.error("Graphic link failure.")
                else:
                    st.warning("Visualizer offline. (OpenAI Key missing or expired)")

            # B. STANDARD COMMAND / SATELLITE SEARCH
            else:
                with st.spinner("Analyzing data streams..."):
                    # Calling your tools.py web search
                    context = tools.web_search(prompt)
                    
                    try:
                        ans = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "You are FRIDAY. You are witty, efficient, and loyal. Always call the user 'Boss'. Avoid robot-like speech."},
                                {"role": "user", "content": f"Satellite Data: {context}\\n\\nUser Command: {prompt}"}
                            ]
                        ).choices[0].message.content
                        
                        st.markdown(ans)
                        speak(ans)
                        st.session_state.messages.append({"role": "assistant", "type": "text", "content": ans})
                    except Exception as e:
                        st.error(f"Neural link broken: {e}")
