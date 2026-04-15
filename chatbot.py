import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
import openai
import tools  # Ensure tools.py is in your GitHub!

# --- 1. HUD & STYLE ---
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

# --- 2. CLIENTS ---
def get_clients():
    try:
        g = Groq(api_key=st.secrets["GROQ_API_KEY"])
        o = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) if "OPENAI_API_KEY" in st.secrets else None
        return g, o
    except Exception as e:
        st.error(f"Keys missing: {e}")
        return None, None

client, openai_client = get_clients()

# --- 3. FRIDAY VOICE (FORCED FEMALE) ---
def speak(text):
    clean = text.replace("'", "").replace("\n", " ").replace('"', '')
    st.components.v1.html(f"""
        <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean}');
        function setVoice() {{
            var voices = window.speechSynthesis.getVoices();
            // Specifically hunting for female tones
            var female = voices.find(v => v.name.includes('Female') || v.name.includes('Hazel') || v.name.includes('Zira') || v.name.includes('Google UK English Female') || v.name.includes('Microsoft Maria'));
            if (female) msg.voice = female;
            msg.rate = 1.05; msg.pitch = 1.2;
            window.speechSynthesis.speak(msg);
        }}
        if (window.speechSynthesis.getVoices().length !== 0) {{ setVoice(); }}
        else {{ window.speechSynthesis.onvoiceschanged = setVoice; }}
        </script>
    """, height=0)

# --- 4. BOOT SEQUENCE ---
if 'booted' not in st.session_state:
    st.session_state.booted = True
    speak("Systems recalibrated. I'm back, Boss. Sorry for the glitch.")

# --- 5. CHAT ENGINE ---
if st.session_state.get('booted'):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if m["type"] == "text": st.markdown(m["content"])
            else: st.image(m["content"])

    if prompt := st.chat_input("Command FRIDAY..."):
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # A. DRAWING LOGIC
            if any(k in prompt.lower() for k in ["draw", "visualize", "show me"]):
                if openai_client:
                    with st.spinner("Rendering..."):
                        try:
                            res = openai_client.images.generate(model="dall-e-3", prompt=prompt)
                            url = res.data[0].url
                            st.image(url)
                            st.session_state.messages.append({"role": "assistant", "type": "image", "content": url})
                            speak("Visualization uploaded to your HUD, Boss.")
                        except: st.error("Visualizer failure.")
                else: st.warning("Visualizer offline.")

            # B. CONVERSATION LOGIC (FRIDAY'S PERSONALITY)
            else:
                with st.spinner("Thinking..."):
                    context = tools.web_search(prompt)
                    
                    # SYSTEM PROMPT - This is where she remembers she's FRIDAY
                    # Put your name in the system content below if you want her to never forget it!
                    ans = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are FRIDAY, Tony Stark's advanced AI. You are witty, efficient, and loyal. Always call the user 'Boss'. Never act like a generic robot."},
                            {"role": "user", "content": f"Context: {context}\nUser says: {prompt}"}
                        ]
                    ).choices[0].message.content
                    
                    st.markdown(ans)
                    speak(ans)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": ans})
