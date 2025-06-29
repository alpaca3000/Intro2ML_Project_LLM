from streamlit_modal import Modal
import streamlit as st

def confirm_modal(
    modal: Modal,
    message: str,
    confirm_label: str,
    on_confirm_callback,
    session_key: str,
):
    """
    Hiển thị modal xác nhận chỉ với nút xác nhận (không có nút Hủy).

    Args:
        modal (Modal): Modal từ streamlit_modal.
        message (str): Nội dung xác nhận.
        confirm_label (str): Nhãn nút xác nhận.
        on_confirm_callback (callable): Hàm gọi khi xác nhận.
        session_key (str): Key session_state cho trạng thái.
    """
    def confirm_action():
        success, msg = on_confirm_callback()
        st.session_state[f"{session_key}_message"] = msg
        st.session_state[f"{session_key}_success"] = success
        modal.close()

    with modal.container():
        st.markdown(
            f"<p style='text-align: center'>{message}</p>",
            unsafe_allow_html=True
        )
        st.button(confirm_label, key=f"{session_key}_confirm", use_container_width=True, on_click=confirm_action)

def toast(session_key: str):
    """
    Hiển thị thông báo toast trong Streamlit.

    Args:
        message (str): Nội dung thông báo.
        success (bool): Trạng thái thành công của thông báo.
    """
    msg_key = f"{session_key}_message"
    success_key = f"{session_key}_success"
    if msg_key in st.session_state:
        if st.session_state[success_key]:
            st.toast(st.session_state[msg_key], icon="✅")
        else:
            st.toast(st.session_state[msg_key], icon="❌")
        del st.session_state[msg_key]
        del st.session_state[success_key]
