import streamlit as st
import time
from services.auth import register_user, login_user

st.set_page_config(page_title="Thông tin người dùng", layout="centered")

# init session state for user tracking 
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# init session state for form input layout
if "show_register_form" not in st.session_state:
    st.session_state.show_register_form = False
if "show_login_form" not in st.session_state:
    st.session_state.show_login_form = False

# --- Nếu đã đăng nhập ---
if st.session_state.is_logged_in:
    st.markdown(f"## Xin chào {st.session_state.username}!")
    st.write("Đây là trang thông tin của bạn.")
    st.sidebar.title(f"Xin chào {st.session_state.username}!")

    if st.button("Đăng xuất", use_container_width=True, icon="🚪"):
        st.session_state.is_logged_in = False
        print(f"[LOG] User {st.session_state.username} logged out successfully.")
        st.session_state.username = None
        st.session_state.user_id = None
        # show thông báo là đang đăng xuất cho người dùng
        st.success("Đang đăng xuất khỏi tài khoản của bạn...")
        time.sleep(1.5)
        st.rerun()

# --- Nếu chưa đăng nhập ---
else:
    st.warning("Bạn chưa đăng nhập. Vui lòng đăng nhập hoặc đăng ký nếu chưa có tài khoản.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Đăng ký", use_container_width=True, icon="📝"):
            st.session_state.show_register_form = True
            st.session_state.show_login_form = False
    with col2:
        if st.button("Đăng nhập", use_container_width=True, icon="🔐"):
            st.session_state.show_login_form = True
            st.session_state.show_register_form = False

    # --- Form Đăng ký ---
    if st.session_state.show_register_form:
        with st.form("register_form"):
            st.subheader("Thông tin đăng ký")
            username = st.text_input("Tên người dùng")
            email = st.text_input("Email")
            password = st.text_input("Mật khẩu", type="password")
            submit = st.form_submit_button("Đăng ký", use_container_width=True)
            if submit:
                if not username or not email or not password:
                    st.warning("Vui lòng điền đầy đủ thông tin.")
                else:
                    result, msg = register_user(username, password, email)
                    if result:
                        st.success("Đăng ký thành công! Vui lòng đăng nhập tài khoản của bạn.")
                        st.session_state.show_register_form = False
                        st.session_state.show_login_form = True
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(msg)

    # --- Form Đăng nhập ---
    if st.session_state.show_login_form:
        with st.form("login_form"):
            st.subheader("Thông tin đăng nhập")
            username = st.text_input("Tên người dùng")
            password = st.text_input("Mật khẩu", type="password")
            submit = st.form_submit_button("Đăng nhập", use_container_width=True)
            if submit:
                if not username or not password:
                    st.warning("Vui lòng điền đầy đủ thông tin.")
                else: 
                    result, msg = login_user(username, password)
                    if result:
                        st.success("Đăng nhập thành công! Chào mừng bạn trở lại.")
                        st.session_state.is_logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = msg
                        st.session_state.show_login_form = False
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(msg)