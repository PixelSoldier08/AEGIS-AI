from tavily import TavilyClient
import streamlit as st

def web_search(query):
    """Gives AEGIS access to real-time news and updates."""
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
    # This searches the web and returns a clean summary for the AI
    response = tavily.search(query=query, search_depth="basic")
    
    # We combine the search results into a simple string
    context = "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in response['results']])
    return context
