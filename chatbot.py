import streamlit as st
from groq import Groq
import tools

# --- 1. HUD & STARK INTERFACE CSS ---
st.set_page_config(page_title="AEGIS GLOBAL HUB", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at center, #0a192f 0%, #050a10 100%);
        color: #00d4ff;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Glowing Chat Bubbles */
    .stChatMessage {
        border: 1px solid #00d4ff;
        box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.2);
        border-radius: 10px;
        background: rgba(10, 25, 47, 0.8) !important;
        margin-bottom: 15px;
    }

    /* Sidebar HUD Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(5, 10, 16, 0.95);
        border-right: 2px solid #00d4ff;
    }

    /* Input Box Customization */
    .stChatInputContainer {
        border-top: 1px solid #00d4ff !important;
        background: transparent !important;
    }
    
    h1, h2, h3 {
        text-shadow: 0px 0px 10px #00d4ff;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE BRAIN INITIALIZATION ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ NEURAL LINK FAILURE: API KEY MISSING")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. SIDEBAR HUD ---
with st.sidebar:
    st.title("💠 AEGIS HUD")
    st.write("---")
    st.write("🛰️ **NETWORK:** SECURE")
    st.write("🧠 **BRAIN:** LLAMA 3.1 INSTANT")
    st.write("🔊 **AUDIO:** OPTIMIZED")
    st.write("📍 **LOC:** TIRUCHIRAPPALLI")
    
    if st.button("🔴 RESET CORE"):
        st.session_state.messages = []
        st.rerun()

# --- 4. INTERACTION LOOP ---
st.title("COMMAND INTERFACE")

# Display Conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Input command for AEGIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # ROUTING: Tool Check
        context = ""
        live_keywords = ["news", "today", "update", "latest", "weather", "who is"]
        
        if any(w in prompt.lower() for w in live_keywords):
            with st.status("📡 Scanning External Satellite Data..."):
                context = tools.web_search(prompt)
        
        if "orbit" in prompt.lower() or "velocity" in prompt.lower():
            nums = "".join(filter(str.isdigit, prompt))
            if nums:
                context = tools.calculate_orbital_mechanics(nums)

        # NEURAL PROCESSING
        final_prompt = f"Context: {context}\n\nUser: {prompt}" if context else prompt
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are AEGIS, a sophisticated JARVIS-style AI. Be tactical, intelligent, and use technical terminology appropriate for a Physics student."}
            ] + st.session_state.messages[:-1] + [{"role": "user", "content": final_prompt}],
            model="llama-3.1-8b-instant",
        )
        
        reply = chat_completion.choices[0].message.content
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # --- TUNED AUDIO OUTPUT ---
        # Pitch 0.9 for depth, Rate 1.1 for tactical speed
        audio_js = f"""
        <script>
        var speech = new SpeechSynthesisUtterance("{reply.replace('"', '').replace("'", "")}");
        speech.pitch = 0.9;
        speech.rate = 1.1;
        speech.volume = 1;
        window.speechSynthesis.speak(speech);
        </script>
        """
        st.components.v1.html(audio_js, height=0)
