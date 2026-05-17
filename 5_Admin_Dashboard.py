import streamlit as st
from auth import authenticate
from database import get_connection
import pandas as pd

def render():
    st.title("Admin Dashboard")
    if "logged_in" not in st.session_state:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.success("Logged in!")
            else:
                st.error("Invalid credentials")
        return

    st.subheader("Add Product")
    name = st.text_input("Product Name")
    desc = st.text_area("Description")
    price = st.number_input("Price")
    image_url = st.text_input("Image URL")
    available = st.checkbox("Available", value=True)
    if st.button("Add Product"):
        conn = get_connection()
        conn.execute("INSERT INTO products (name, description, price, image_url, available) VALUES (?, ?, ?, ?, ?)",
                     (name, desc, price, image_url, int(available)))
        conn.commit()
        conn.close()
        st.success("Product added")

    st.subheader("Existing Products")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM products", conn)
    st.dataframe(df)
    conn.close()

    st.subheader("Google Integration")
    ads_id = st.text_input("Google Ads ID")
    ga_id = st.text_input("GA4 Measurement ID")
    if ads_id and ga_id:
        from ga_integration import inject_tracking
        inject_tracking(ads_id, ga_id)
        st.success("Tracking scripts injected")