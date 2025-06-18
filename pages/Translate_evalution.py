import streamlit as st
from services.translate import evaluate_translation
from utils.session import is_logged_in

# Khởi tạo biến session cho check button
for key in ["percentage_correct", "model_translation", "show_result"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "show_result" else False

# tiêu đề trang
st.title("Đánh giá khả năng dịch của bạn")

# kiểm tra xem người dùng đã đăng nhập chưa
if not is_logged_in():
    st.warning("Bạn cần đăng nhập để thực hiện chức năng này.")
    st.stop()

st.sidebar.title(f"Xin chào {st.session_state.username}!")

# --- Nhập văn bản ---
english_text = st.text_area("Nhập văn bản tiếng Anh:", "hello world!")

# Nếu chưa có kết quả, cho nhập bản dịch
if not st.session_state.show_result:
    user_input = st.text_area("Nhập bản dịch của bạn:")

    blank_col, eval_col = st.columns([3, 1])
    with eval_col:
        if st.button("Đánh giá", use_container_width=True, icon="🔍"):
            if not user_input.strip():
                st.warning("⚠️ Vui lòng nhập bản dịch.")
            else:
                percent, translation = evaluate_translation(english_text, user_input)
                st.session_state.percentage_correct = percent
                st.session_state.model_translation = translation
                st.session_state.show_result = True

# --- Kết quả sau khi đánh giá ---
if st.session_state.show_result:
    percent = st.session_state.percentage_correct
    if percent >= 80:
        st.success(f"✅ Bản dịch của bạn chính xác {percent:.2f}%")
    else:
        st.error(f"🚫 Bản dịch của bạn chỉ chính xác {percent:.2f}%.")

    # nút đánh giá lại: bạn có muốn thử lại không?
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.write("Bạn có muốn thử lại không?")
    with col_right:
        if st.button("🔁 Thử lại"):
            st.session_state.percentage_correct = None
            st.session_state.model_translation = None
            st.session_state.show_result = False
            st.rerun()

    # Hiển thị tùy chọn xem bản dịch hệ thống
    with st.expander("👁 Xem bản dịch của hệ thống?"):
        # st.info("Đây là bản dịch gợi ý từ hệ thống:")
        st.info(st.session_state.model_translation)