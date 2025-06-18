import streamlit as st

def is_logged_in():
    return st.session_state.get("is_logged_in", False)