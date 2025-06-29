import streamlit as st

def is_logged_in():
    return st.session_state.get("is_logged_in", False)

# --- Callback Functions cho trang Tài khoản của tôi---
def show_register():
    st.session_state.show_register_form = True
    st.session_state.show_login_form = False

def show_login():
    st.session_state.show_login_form = True
    st.session_state.show_register_form = False

def logout():
    st.session_state.is_logged_in = False
    st.session_state.username = None
    st.session_state.user_id = None
    st.session_state.show_login_form = False
    st.session_state.show_register_form = False
    st.toast("Đăng xuất thành công!", icon="✅")
