import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
import openai
import tools  # This links to your tools.py file

# --- HUD & STYLE ---
st.set_page_config(page_title="AEGIS: FRIDAY PROTOCOL", layout="wide")
st.markdown("<style>.stApp { background-color: #060b14; color: #ff3399; }</style>", unsafe_allow_html=True)

# --- CLIENTS ---
def get_clients():
    try:
        g = Groq(api_key=st.secrets["GROQ_API_KEY"])
        o = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) if "OPENAI_API_KEY" in st.secrets else None
        return g, o
    except: return None, None

client, openai_client = get_clients()

# --- FRIDAY VOICE ---
def speak(text):
    clean = text.replace("'", "").replace("\n", " ")
    st.components.v1.html(f"""
        <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean}');
        var voices = window.speechSynthesis.getVoices();
        msg.voice = voices.find(v => v.name.includes('Female') || v.name.includes('Hazel') || v.name.includes('Google UK English Female'));
        msg.rate = 1.1; msg.pitch = 1.2;
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- BOOT ---
if 'booted' not in st.session_state:
    with st.spinner("Initializing Friday..."):
        time.sleep(2)
        speak("All systems green, Boss.")
    st.session_state.booted = True

# --- CHAT ---
if st.session_state.get('booted'):
    if "messages" not in st.session_state: st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if m["type"] == "text": st.markdown(m["content"])
            else: st.image(m["content"])

    if prompt := st.chat_input("Command FRIDAY..."):
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # DRAWING LOGIC
            if any(k in prompt.lower() for k in ["draw", "visualize", "show me"]):
                if openai_client:
                    with st.spinner("Visualizing..."):
                        try:
                            res = openai_client.images.generate(model="dall-e-3", prompt=prompt, n=1)
                            url = res.data[0].url
                            st.image(url)
                            st.session_state.messages.append({"role": "assistant", "type": "image", "content": url})
                            speak("Visualization complete.")
                        except: st.error("Image generation failed.")
                else: st.warning("Visualizer key missing.")
            
            # TEXT LOGIC
            else:
                context = tools.web_search(prompt)
                ans = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": f"You are FRIDAY. Context: {context}"}, {"role": "user", "content": prompt}]
                ).choices[0].message.content
                st.markdown(ans)
                speak(ans)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": ans})
