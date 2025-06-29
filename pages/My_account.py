import streamlit as st
import time
from services.auth import register_user, login_user
from utils.session import is_logged_in

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

st.title("TÀI KHOẢN CỦA TÔI")

# --- Khởi tạo session state ---
for key, value in {
    "is_logged_in": False,
    "username": None,
    "user_id": None,
    "show_register_form": False,
    "show_login_form": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Nếu đã đăng nhập ---
if is_logged_in():
    st.markdown(f"## Xin chào {st.session_state.username}!")
    st.write("Đây là trang thông tin của bạn.")
    st.sidebar.title(f"Xin chào {st.session_state.username}!")

    st.button("Đăng xuất", use_container_width=True, icon="🚪", on_click=logout)
    time.sleep(1)

# --- Nếu chưa đăng nhập ---
else:
    st.warning("Bạn chưa đăng nhập. Vui lòng đăng nhập hoặc đăng ký nếu chưa có tài khoản.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Đăng ký", use_container_width=True, icon="📝", on_click=show_register)
    with col2:
        st.button("Đăng nhập", use_container_width=True, icon="🔐", on_click=show_login)

    # --- Form Đăng ký ---
    if st.session_state.show_register_form:
        with st.form("register_form"):
            st.subheader("Thông tin đăng ký")
            username = st.text_input("Tên người dùng")
            email = st.text_input("Email")
            password = st.text_input("Mật khẩu", type="password")
            submit = st.form_submit_button("Đăng ký", use_container_width=True, icon="📝")
            if submit:
                if not username or not email or not password:
                    st.warning("Vui lòng điền đầy đủ thông tin.")
                else:
                    result, msg = register_user(username, password, email)
                    if result:
                        st.toast("Đăng ký thành công! Vui lòng đăng nhập tài khoản của bạn.", icon="✅")
                        st.session_state.show_register_form = False
                        st.session_state.show_login_form = True
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(msg)

    # --- Form Đăng nhập ---
    if st.session_state.show_login_form:
        with st.form("login_form"):
            st.subheader("Thông tin đăng nhập")
            username = st.text_input("Tên người dùng")
            password = st.text_input("Mật khẩu", type="password")
            submit = st.form_submit_button("Đăng nhập", use_container_width=True, icon="🔑")
            if submit:
                if not username or not password:
                    st.warning("Vui lòng điền đầy đủ thông tin.")
                else:
                    result, msg = login_user(username, password)
                    if result:
                        st.toast("Đăng nhập thành công! Chào mừng bạn trở lại.", icon="✅")
                        st.session_state.is_logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = msg
                        st.session_state.show_login_form = False
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(msg)