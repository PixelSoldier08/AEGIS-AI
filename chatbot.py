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
    except:
        return None, None

client, openai_client = get_clients()

# --- 3. CLEAN VOICE PROTOCOL (No Noise Fix) ---
def speak(text):
    # Removing special characters that cause "static" or glitches in JS
    clean = text.replace("'", "").replace('"', "").replace("\n", " ").replace("*", "")
    st.components.v1.html(f"""
        <script>
        window.speechSynthesis.cancel(); // Clears queue to prevent overlapping noise
        setTimeout(() => {{
            var msg = new SpeechSynthesisUtterance('{clean}');
            var voices = window.speechSynthesis.getVoices();
            var female = voices.find(v => v.name.includes('Female') || v.name.includes('Hazel') || v.name.includes('Google UK English Female'));
            if (female) msg.voice = female;
            msg.rate = 1.0; msg.pitch = 1.2;
            window.speechSynthesis.speak(msg);
        }}, 100);
        </script>
    """, height=0)

# --- 4. THE BOOT SEQUENCE (Fixed Visibility) ---
if 'booted' not in st.session_state:
    # Use a placeholder to ensure it shows up before anything else
    boot_placeholder = st.empty()
    with boot_placeholder.container():
        res = requests.get("https://lottie.host/809c7333-e7f3-4d6d-9653-6a9b441f7e02/B79P5J1w8G.json")
        lottie_json = res.json() if res.status_code == 200 else None
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if lottie_json:
                st_lottie(lottie_json, height=350, key="boot_anim")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            load_steps = [
                ("INITIALIZING HUD...", 25),
                ("SYNCING NEURAL NET...", 50),
                ("DECRYPTING SATELLITE DATA...", 75),
                ("FRIDAY ONLINE.", 100)
            ]
            
            for step, val in load_steps:
                status_text.markdown(f"**`{step}`**")
                progress_bar.progress(val)
                time.sleep(0.8)
            
            speak("Systems fully operational, Boss. I'm ready when you are.")
            time.sleep(1) 
    
    st.session_state.booted = True
    boot_placeholder.empty() # Clears the boot screen to show the chat

# --- 5. MAIN CHAT INTERFACE ---
if st.session_state.get('booted'):
    st.title("AEGIS: FRIDAY PROTOCOL")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            if m["type"] == "text": st.markdown(m["content"])
            else: st.image(m["content"])

    if prompt := st.chat_input("What's the plan, Boss?"):
        st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            # DRAWING LOGIC
            if any(k in prompt.lower() for k in ["draw", "visualize", "show me"]):
                if openai_client:
                    with st.spinner("Rendering Visuals..."):
                        try:
                            res = openai_client.images.generate(model="dall-e-3", prompt=prompt)
                            url = res.data[0].url
                            st.image(url)
                            st.session_state.messages.append({"role": "assistant", "type": "image", "content": url})
                            speak("Check your display, Boss.")
                        except: st.error("Graphic drivers failed.")
                else: st.warning("Visualizer offline.")

            # TEXT LOGIC
            else:
                with st.spinner("Processing..."):
                    context = tools.web_search(prompt)
                    ans = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are FRIDAY. You are efficient, loyal, and witty. Always call the user 'Boss'."},
                            {"role": "user", "content": f"Context: {context}\n\n{prompt}"}
                        ]
                    ).choices[0].message.content
                    
                    st.markdown(ans)
                    speak(ans)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": ans})
