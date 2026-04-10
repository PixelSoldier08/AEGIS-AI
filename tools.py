import math
import streamlit as st
from tavily import TavilyClient

def web_search(query):
    """Accesses the web via Tavily API."""
    try:
        tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        response = tavily.search(query=query, search_depth="basic", max_results=3)
        return "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in response['results']])
    except Exception as e:
        return f"Satellite link error: {str(e)}"

def calculate_orbital_mechanics(r_km):
    """Physics engine for orbital calculations."""
    try:
        G = 6.67430e-11
        M = 5.972e24
        r = (float(r_km) + 6371) * 1000 
        v = math.sqrt((G * M) / r)
        return f"Tactical Data: Orbital Velocity at altitude {r_km}km is {round(v, 2)} m/s."
    except:
        return "Calculation error in orbital parameters."
