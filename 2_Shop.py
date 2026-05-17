import streamlit as st
import pandas as pd
from database import get_connection

def render():
    st.title("Shop")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM products WHERE available = 1", conn)
    for _, row in df.iterrows():
        st.image(row['image_url'], width=200)
        st.subheader(row['name'])
        st.write(row['description'])
        st.write(f"₹ {row['price']}")
        st.button("Add to Cart", key=f"add_{row['id']}")
    conn.close()