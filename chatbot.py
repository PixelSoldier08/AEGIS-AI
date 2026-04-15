import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
import openai
import tools # Using your local tools.py

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
    </style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZE CLIENTS ---
def get_clients():
    try:
        g = Groq(api_key=st.secrets["GROQ_API_KEY"])
        # Only start OpenAI if the key exists
        o = None
        if "OPENAI_API_KEY" in st.secrets:
            o = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        return g, o
    except Exception as e:
        st.error(f"Boss, API keys are missing! {e}")
        return None, None

client, openai_client = get_clients()

# --- 3. VOICE PROTOCOL (Stop on Tab Switch) ---
def speak(text):
    clean = text.replace("'", "").replace('"', "").replace("\n", " ").replace("*", "")
    st.components.v1.html(f"""
        <script>
        window.speechSynthesis.cancel(); 
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{ window.speechSynthesis.cancel(); }}
        }});
        setTimeout(() => {{
            var msg = new SpeechSynthesisUtterance('{clean}');
            var voices = window.speechSynthesis.getVoices();
            var female = voices.find(v => v.name.includes('Female') || v.name.includes('Hazel') || v.name.includes('Google UK English Female'));
            if (female) msg.voice = female;
            msg.rate = 1.0; msg.pitch = 1.2;
            window.speechSynthesis.speak(msg);
        }}, 50);
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
            if lottie_json: st_lottie(lottie_json, height=350, key="boot_anim")
            progress_bar = st.progress(0)
            status_text = st.empty()
            for step, val in [("INITIALIZING...", 33), ("SYNCING...", 66), ("ONLINE.", 100)]:
                status_text.markdown(f"**`{step}`**")
                progress_bar.progress(val)
                time.sleep(0.6)
            speak("Welcome back, Boss.")
    st.session_state.booted = True
    boot_placeholder.empty()

# --- 5. CHAT ENGINE ---
if st.session_state.get('booted'):
    st.title("AEGIS: FRIDAY PROTOCOL")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if m["type"] == "text": st.markdown(m["content"])
            else: st.image(m["content"])

    if prompt := st.chat_input("Command FRIDAY..."):
        # Stop previous audio immediately
        st.components.v1.html("<script>window.speechSynthesis.cancel();</script>", height=0)
        
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # --- CHOICE 1: IMAGE GENERATION ---
            if any(k in prompt.lower() for k in ["draw", "visualize", "image", "show me a picture"]):
                if openai_client:
                    with st.spinner("Accessing visual sub-routines..."):
                        try:
                            res = openai_client.images.generate(
                                model="dall-e-3",
                                prompt=f"Marvel cinematic style: {prompt}",
                                n=1
                            )
                            url = res.data[0].url
                            st.image(url)
                            st.session_state.messages.append({"role": "assistant", "type": "image", "content": url})
                            speak("The visualization is ready for your review, Boss.")
                        except Exception as e:
                            st.error(f"Visualizer error: {e}")
                else:
                    st.warning("Boss, I need an OpenAI API key in Secrets to generate images.")

            # --- CHOICE 2: CONVERSATION ---
            else:
                with st.spinner("Processing..."):
                    context = tools.web_search(prompt)
                    ans = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are FRIDAY. Be witty, loyal, and call the user Boss."},
                            {"role": "user", "content": f"Context: {context}\\n\\n{prompt}"}
                        ]
                    ).choices[0].message.content
                    
                    st.markdown(ans)
                    speak(ans)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": ans})
