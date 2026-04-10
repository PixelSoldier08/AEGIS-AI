import math
import streamlit as st
from tavily import TavilyClient

# --- LIVE WEB SEARCH ---
def web_search(query):
    """Gives AEGIS access to real-time news and updates."""
    try:
        tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        # Optimized for LLM context
        response = tavily.search(query=query, search_depth="basic", max_results=3)
        context = "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in response['results']])
        return context
    except Exception as e:
        return f"Search System Error: {str(e)}"

# --- PHYSICS ENGINE ---
def calculate_orbital_mechanics(r_km):
    """Accurate orbital math for B.Sc. studies."""
    try:
        G = 6.67430e-11
        M = 5.972e24
        r = (float(r_km) + 6371) * 1000  # Altitude to radius in meters
        v = math.sqrt((G * M) / r)
        return f"Orbital Velocity at {r_km}km: {round(v, 2)} m/s"
    except:
        return "Calculation Error: Please provide a valid altitude."
