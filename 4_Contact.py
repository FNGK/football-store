import streamlit as st

def render():
    st.title("Contact Us")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    msg = st.text_area("Your Message")
    if st.button("Send"):
        st.success("Message sent!")