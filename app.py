import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Insight Flow Dashboard", layout="wide")

# --- MAIN UI ---
st.title("🚀 Insight Flow - Lead Hunter & Auditor")
st.subheader("Welcome Hafiz! Your Cloud Agency is Live.")

st.sidebar.header("Targeting")
niche = st.sidebar.text_input("Niche", "Real Estate")
limit = st.sidebar.slider("Daily Limit", 10, 100, 50)

if st.button("🔥 Run Hunter"):
    st.info(f"Scanning for {niche} leads...")
    st.success("Bot is running in the cloud! No laptop space needed.")

# Performance Stats
col1, col2 = st.columns(2)
col1.metric("Leads Found", "0")
col2.metric("Emails Sent", "0")

st.markdown("---")
st.write("Current Status: System Integrated with Gmail ✅")
