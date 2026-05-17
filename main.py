import streamlit as st
from auth import authenticate
from utils import load_page

st.set_page_config(page_title="Football Store | fngk.in", layout="wide")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

load_page("1_Home")