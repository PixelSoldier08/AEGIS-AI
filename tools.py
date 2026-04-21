import os
from tavily import TavilyClient

def web_search(query):
    try:
        # Pulls the key we will set in Streamlit Secrets later
        import streamlit as st
        tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
        response = tavily.search(query=query, search_depth="advanced")
        return str(response)
    except Exception as e:
        return f"Satellite search error: {e}"

def calculate_orbital_velocity(altitude_km):
    # Physics Constant for Earth
    GM = 3.986004418e14 
    R = 6371000 + (altitude_km * 1000)
    import math
    velocity = math.sqrt(GM / R)
    return f"Orbital Velocity at {altitude_km}km is {round(velocity, 2)} m/s."
