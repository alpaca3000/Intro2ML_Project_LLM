import streamlit as st
from services.translate import translate_text
from services.vocab import add_vocab
from utils.session import is_logged_in

# giới thiệu về trang web envichan
st.title("Chào mừng đến với Envichan!")
st.write("Envichan là một ứng dụng học tiếng Anh trực tuyến, nơi bạn có thể học từ vựng, ngữ pháp và thực hành giao tiếp.")

# hiển thị phần dịch tiếng Anh sang tiếng Việt
st.subheader("Dịch tiếng Anh sang tiếng Việt")
text = st.text_area("Nhập nội dung tiếng Anh:")
blank_col, translate_col = st.columns([4, 1])
with translate_col:
    translate = st.button("Dịch", use_container_width=True)
        
if translate: 
    result = translate_text(text)
    st.success(result)

# hiển thị phần thêm từ vựng
st.subheader("Thêm từ vựng vào từ điển của bạn?")
# kiểm tra xem người dùng đã đăng nhập hay chưa
if not is_logged_in():
    st.warning("Bạn cần đăng nhập để thực hiện chức năng này.")
else:
    st.sidebar.title(f"Xin chào {st.session_state.username}!")
    with st.expander("Nhập thông tin từ vựng mới"):
        with st.form("add_vocab_form", clear_on_submit=True):
            en = st.text_input("Từ tiếng Anh", key="en_input")
            vi = st.text_input("Nghĩa tiếng Việt", key="vi_input")
            word_class = st.selectbox("Loại từ", ["Danh từ", "Động từ", "Tính từ", "Trạng từ"], key="word_class_input")
            example_en = st.text_input("Ví dụ tiếng Anh", key="ex_input")
            example_vi = translate_text(example_en) if example_en else ""
            status = st.selectbox("Trạng thái", ["Đang học", "Đã nhớ"], key="status_input")
            
            # 2 nút thêm và hủy
            left_blank_col, col1, col2, right_blank_col = st.columns([1, 1, 1, 1])
            with col1:
                submit = st.form_submit_button("Thêm", use_container_width=True, type="secondary", icon="➕")
            with col2:
                cancel = st.form_submit_button("Hủy", use_container_width=True, type="secondary", icon="❌")

            # kiểm tra trường thông tin chưa nhập
            if submit:
                if not en or not vi or not word_class or not example_en:
                    st.error("Vui lòng điền đầy đủ thông tin.")
                else:
                    # thêm từ vựng vào cơ sở dữ liệu
                    result, msg = add_vocab(st.session_state["user_id"], en, vi, word_class, example_en, example_vi, status)
                    if result:
                        st.toast(f"Đã thêm {en} vào từ điển của bạn!", icon="✅")
                    else:
                        st.error(f"Lỗi: {msg}")
            if cancel:
                st.rerun()