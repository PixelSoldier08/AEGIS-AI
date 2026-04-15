import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
import openai
import tools 

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
        o = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) if "OPENAI_API_KEY" in st.secrets else None
        return g, o
    except: return None, None

client, openai_client = get_clients()

# --- 3. SMART VOICE PROTOCOL (Clears Queue & Tab Detection) ---
def speak(text):
    clean = text.replace("'", "").replace('"', "").replace("\n", " ").replace("*", "")
    st.components.v1.html(f"""
        <script>
        // 1. Immediate cancel of previous speech
        window.speechSynthesis.cancel(); 

        // 2. Tab Visibility Detection: Stop speaking if user leaves tab
        document.addEventListener("visibilitychange", function() {{
            if (document.hidden) {{
                window.speechSynthesis.cancel();
            }}
        }});

        // 3. Optimized Speech trigger
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
            
            speak("All systems online, Boss.")
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
        # Reset vocal queue on new input
        st.components.v1.html("<script>window.speechSynthesis.cancel();</script>", height=0)
        
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            if any(k in prompt.lower() for k in ["draw", "visualize", "image"]):
                if openai_client:
                    with st.spinner("Visualizing..."):
                        try:
                            res = openai_client.images.generate(model="dall-e-3", prompt=prompt)
                            url = res.data[0].url
                            st.image(url)
                            st.session_state.messages.append({"role": "assistant", "type": "image", "content": url})
                            speak("Visualization ready, Boss.")
                        except: st.error("Image generation failed.")
                else: st.warning("Visualizer offline.")
            else:
                with st.spinner("Thinking..."):
                    context = tools.web_search(prompt)
                    ans = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are FRIDAY. Be efficient and call the user Boss."},
                            {"role": "user", "content": f"Context: {context}\\n\\n{prompt}"}
                        ]
                    ).choices[0].message.content
                    
                    st.markdown(ans)
                    speak(ans)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": ans})
