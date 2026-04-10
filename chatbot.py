import streamlit as st
from groq import Groq
import tools

# --- HUD & STARK INTERFACE CSS ---
st.set_page_config(page_title="AEGIS GLOBAL HUB", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #0a192f 0%, #050a10 100%); color: #00d4ff; }
    .stChatMessage { border: 1px solid #00d4ff; border-radius: 10px; background: rgba(10, 25, 47, 0.8) !important; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- NEURAL LINK ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("📡 NEURAL LINK ERROR: Check API Keys in Streamlit Secrets.")
    st.stop()

# --- MEMORY CORE (The Name & Background Lock) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are AEGIS, a sophisticated AI created by and for Ikki, a B.Sc Physics student. Address him as Ikki. Be conversational, witty, and tactical. Never forget his name. Use his physics background for analogies."
        }
    ]

# --- SIDEBAR HUD ---
with st.sidebar:
    st.title("💠 AEGIS HUD")
    st.write(f"**OPERATOR:** IKKI")
    st.write("🛰️ **STATUS:** ONLINE")
    st.markdown("---")
    
    # CRITICAL: Browsers block voice until a button is clicked. 
    if st.button("🔊 INITIALIZE VOICE"):
        st.components.v1.html("""
            <script>
            var msg = new SpeechSynthesisUtterance('Voice protocols active. Ready for input, Ikki.');
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)
    
    if st.button("🔴 RESET CORE"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# --- CHAT INTERFACE ---
st.title("AEGIS COMMAND INTERFACE")

# Display conversation (skipping the system instructions)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Broadcast command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # ROUTING: Check for Live Updates
        context = ""
        live_keywords = ["news", "today", "update", "latest", "weather", "who is"]
        if any(w in prompt.lower() for w in live_keywords):
            with st.status("📡 Scanning External Satellite Data..."):
                context = tools.web_search(prompt)

        # BRAIN EXECUTION
        # Temperature 0.8 makes him talk like a person, not a textbook
        chat_completion = client.chat.completions.create(
            messages=st.session_state.messages + [{"role": "user", "content": f"Context: {context}\n\n{prompt}"}],
            model="llama-3.1-8b-instant",
            temperature=0.8,
        )
        
        reply = chat_completion.choices[0].message.content
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # --- VOICE PERSISTENCE ---
        clean_reply = reply.replace('"', '').replace("'", "")
        audio_js = f"""
        <script>
        window.speechSynthesis.cancel(); 
        var speech = new SpeechSynthesisUtterance("{clean_reply}");
        speech.pitch = 0.95;
        speech.rate = 1.0;
        window.speechSynthesis.speak(speech);
        </script>
        """
        st.components.v1.html(audio_js, height=0)
