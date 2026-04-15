import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie
from groq import Groq
import openai
import tools 

# --- 1. HUD & STYLING (The Glowing Effect) ---
st.set_page_config(page_title="AEGIS: FRIDAY PROTOCOL", layout="wide")

st.markdown("""
    <style>
    /* Dark Background */
    .stApp { 
        background-color: #060b14; 
        color: #ff3399; 
    }
    
    /* Glowing Neon Cyan Text */
    .stMarkdown, p, h1, h2, h3, li { 
        color: #00f2ff !important; 
        text-shadow: 0 0 12px rgba(0, 242, 255, 0.8), 0 0 5px rgba(0, 242, 255, 0.5);
        font-family: 'Courier New', monospace;
    }

    /* Chat Message Boxes */
    [data-testid="stChatMessage"] {
        background: rgba(0, 242, 255, 0.05) !important;
        border: 1px solid rgba(0, 242, 255, 0.2) !important;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
    }

    /* Input Box Styling */
    .stChatInputContainer {
        border-top: 1px solid #ff3399 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE REST OF YOUR CLIENTS ---
# (Keep your get_clients() and speak() functions here as they were before)
