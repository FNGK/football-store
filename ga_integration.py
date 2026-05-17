import streamlit as st

def inject_tracking(ads_id, ga_id):
    st.markdown(f"""
    <!-- Google Ads -->
    <script async src='https://www.googletagmanager.com/gtag/js?id={ads_id}'></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_id}');
    </script>
    """, unsafe_allow_html=True)