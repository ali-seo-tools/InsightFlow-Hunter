import streamlit as st
import asyncio
from insight_hunter import universal_power_hunter

# --- PAGE CONFIG ---
st.set_page_config(page_title="InsightFlow Global Auditor", layout="wide")

st.title("🌐 Worldwide Lead Discovery & Tracking Audit")
st.subheader("Welcome Hafiz! Your Global Agency is Live.")

# --- SIDEBAR OPTIONS ---
st.sidebar.header("Targeting Parameters")
category = st.sidebar.selectbox(
    "Select Industry:",
    ["Real Estate", "Law Firms", "Medical Spa", "Roofing Contractors", "Dental Clinics", "E-commerce", "Custom Niche"]
)

if category == "Custom Niche":
    niche_to_search = st.sidebar.text_input("Enter Industry Name:")
else:
    niche_to_search = category

location = st.sidebar.text_input("Target Location (e.g., USA, UK, Dubai):", "USA")
scan_limit = st.sidebar.slider("Number of leads to scan", 5, 50, 10)

# --- MAIN ACTION ---
if st.sidebar.button("🚀 Start Global Scan"):
    if not niche_to_search:
        st.error("Please enter a niche.")
    else:
        st.info(f"Scanning the web for {niche_to_search} in {location}...")
        
        # Calling the Python Brain
        with st.spinner("Analyzing websites..."):
            results = asyncio.run(universal_power_hunter(niche_to_search, location, scan_limit))
            
            if results:
                st.success(f"Scan Complete! Found {len(results)} leads.")
                st.table(results) # Asli Audit Report dikhaye ga
            else:
                st.warning("No leads found. Try different keywords.")
