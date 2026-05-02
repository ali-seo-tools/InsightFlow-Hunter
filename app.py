import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import urllib.parse

WHATSAPP_NUMBER = "923119883980"
SHEETMONKEY_URL = "https://api.sheetmonkey.io/form/pfXXGEq1dfsfH95fWqx6Vd"

st.set_page_config(page_title="InsightFlow Hunter - Free Audit", page_icon="🔍")

st.markdown("""
<style>
.score-circle {
    width: 140px; height: 140px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 2.8rem; font-weight: 800; margin: 20px auto;
    background: #e5e7eb; color: #111;
}
.red { background: #f8d7da; color: #842029; }
.orange { background: #fff3cd; color: #664d03; }
.green { background: #d1e7dd; color: #0f5132; }
.issue-box {
    background: #fef3c7; border-left: 4px solid #f59e0b; padding: 10px;
    margin: 6px 0; border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 InsightFlow Hunter")
st.markdown("### Free GA4, GTM, Meta Pixel & Server‑Side Tracking Audit")
st.markdown("Enter your e‑commerce site URL — get a free health score in 5 seconds")

url = st.text_input("Website URL", placeholder="https://yourstore.com")

if st.button("Scan Now"):
    if url:
        if not url.startswith("http"):
            url = "https://" + url
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            resp = requests.get(url, timeout=15, headers=headers)
            resp.raise_for_status()
            html = resp.text

            ga4_detected = bool(re.search(
                r'(gtag\(\'config\',\s*\'G-[A-Z0-9]+\'\)|googletagmanager\.com/gtag/js\?id=G-)', html))
            gtm_detected = bool(re.search(
                r'googletagmanager\.com/gtm\.js\?id=GTM-\w+', html))
            meta_detected = bool(re.search(
                r'fbq\(\'init\',\s*\'\d+\'\)', html)) or 'connect.facebook.net' in html
            server_hints = bool(re.search(
                r'(server[-_]side|conversion\.api|capig?)', html, re.I))

            ga4_issues = [] if ga4_detected else ["GA4 tracking code missing."]
            gtm_issues = [] if gtm_detected else ["Google Tag Manager snippet not found."]
            meta_issues = [] if meta_detected else ["Meta Pixel base code missing."]
            server_issues = [] if server_hints else ["No server‑side tracking references found."]

            passed = sum([ga4_detected, gtm_detected, meta_detected, server_hints])
            score = int((passed / 4) * 100)

            color_class = "red" if score < 50 else ("orange" if score < 90 else "green")
            st.markdown(f"<div class='score-circle {color_class}'>{score}%</div>", unsafe_allow_html=True)
            st.subheader(f"Tracking Health Score for {url}")

            tab1, tab2, tab3, tab4 = st.tabs(["GA4", "GTM", "Meta Pixel", "Server‑Side"])
            with tab1:
                for issue in ga4_issues:
                    st.markdown(f"<div class='issue-box'>❌ {issue}</div>", unsafe_allow_html=True)
                if not ga4_issues:
                    st.success("✅ GA4 properly configured.")
            with tab2:
                for issue in gtm_issues:
                    st.markdown(f"<div class='issue-box'>❌ {issue}</div>", unsafe_allow_html=True)
                if not gtm_issues:
                    st.success("✅ GTM properly configured.")
            with tab3:
                for issue in meta_issues:
                    st.markdown(f"<div class='issue-box'>❌ {issue}</div>", unsafe_allow_html=True)
                if not meta_issues:
                    st.success("✅ Meta Pixel properly configured.")
            with tab4:
                for issue in server_issues:
                    st.markdown(f"<div class='issue-box'>❌ {issue}</div>", unsafe_allow_html=True)
                if not server_issues:
                    st.success("✅ Server‑side tracking appears to be implemented.")

            st.markdown("---")
            st.subheader("📩 Get Full Audit Report")
            email = st.text_input("Enter your email", placeholder="you@example.com")
            if st.button("Send Report"):
                if email:
                    data = {
                        "Email": email,
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "URL Scanned": url,
                        "Score": score
                    }
                    try:
                        resp_sheet = requests.post(SHEETMONKEY_URL, json=data, timeout=10)
                        if resp_sheet.status_code == 200:
                            st.success("✅ Report sent! Your data has been saved.")
                        else:
                            st.warning("Could not save automatically, but you can contact us on WhatsApp.")
                    except:
                        st.warning("Network issue — please contact us on WhatsApp.")
                else:
                    st.warning("Please enter an email address.")

            wa_text = f"Hi, I want to fix my tracking for {url}"
            wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(wa_text)}"
            st.markdown(
                f'<a href="{wa_link}" target="_blank">'
                f'<button style="background:#25D366; color:white; border:none; '
                f'padding:12px 28px; border-radius:30px; font-size:18px;">'
                f'📱 Chat on WhatsApp</button></a>',
                unsafe_allow_html=True
            )

            st.markdown("---")
            st.subheader("📢 Share Your Score")
            tweet = f"My store's tracking health is only {score}%! Check yours for free: https://insightflow-hunter.streamlit.app"
            fb_link = "https://www.facebook.com/sharer/sharer.php?u=https://insightflow-hunter.streamlit.app"
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f'<a href="https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet)}" target="_blank">'
                    f'<button style="background:#1DA1F2; color:white; padding:10px 20px; border:none; border-radius:30px;">'
                    f'🐦 Twitter/X</button></a>',
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    f'<a href="{fb_link}" target="_blank">'
                    f'<button style="background:#1877F2; color:white; padding:10px 20px; border:none; border-radius:30px;">'
                    f'📘 Facebook</button></a>',
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"Could not scan the site. Reason: {e}")
    else:
        st.warning("Please enter a URL.")
