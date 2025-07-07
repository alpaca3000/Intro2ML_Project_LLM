import streamlit as st
from services.translate import evaluate_translation, get_wordnet_info
from utils.session import is_logged_in

# # Tải dữ liệu WordNet (chỉ chạy lần đầu)
# if not os.path.exists('./nltk_data'):
#     nltk.download('wordnet', download_dir='./nltk_data')
#     nltk.download('punkt', download_dir='./nltk_data')
# nltk.data.path.append('./nltk_data')

# Khởi tạo biến session
for key in ["percentage_correct", "model_translation", "show_result"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "show_result" else False

# Tiêu đề trang
st.title("Đánh giá khả năng dịch của bạn")

# Kiểm tra đăng nhập
if not is_logged_in():
    st.warning("Bạn cần đăng nhập để thực hiện chức năng này.")
    st.stop()

st.sidebar.title(f"Xin chào {st.session_state.username}!")

# Nhập văn bản
english_text = st.text_area("Nhập văn bản tiếng Anh:", "hello world!")

# # Kiểm tra xem văn bản có phải là từ đơn để thêm WordNet
# if len(english_text.split()) == 1:  # Nếu là từ đơn
#     wordnet_info = get_wordnet_info(english_text)
#     if wordnet_info:
#         with st.expander("Thông tin từ điển (WordNet)"):
#             st.write(f"**Định nghĩa (English):** {wordnet_info['definition']}")
#             st.write(f"**Ví dụ (English):** {wordnet_info['examples']}")
#             st.write(f"**Từ đồng nghĩa (English):** {wordnet_info['synonyms']}")

# Nếu chưa có kết quả, cho nhập bản dịch
# if not st.session_state.show_result:
user_input = st.text_area("Nhập bản dịch của bạn:")

blank_col, eval_col = st.columns([3, 1])
with eval_col:
    if st.button("Đánh giá", use_container_width=True, icon="🔍", disabled=(not user_input.strip())):
        st.session_state.show_result = True

if st.session_state.show_result:
    with st.spinner("Đang đánh giá bản dịch..."):  # Thêm spinner
        percent, translation = evaluate_translation(english_text, user_input)
        st.session_state.percentage_correct = percent
        st.session_state.model_translation = translation
        #st.session_state.show_result = False

# Kết quả sau khi đánh giá
if st.session_state.show_result:
    st.session_state.show_result = False
    percent = st.session_state.percentage_correct
    if percent >= 80:
        st.info(f"Bản dịch của bạn có độ chính xác cao với độ phù hợp {percent:.2f}%")
    elif percent >= 50:
        st.info(f"Bạn dịch của bạn có thể chấp nhận được với độ phù hợp {percent:.2f}%")
    else:
        st.info(f"Bản dịch của bạn chỉ chính xác {percent:.2f}%.")

    # Nút thử lại
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.write("Bạn có muốn thử lại không?")
    with col_right:
        if st.button("🔁 Thử lại"):
            st.session_state.percentage_correct = None
            st.session_state.model_translation = None
            st.session_state.show_result = False
            st.session_state.comparison = None
            st.rerun()

    # Hiển thị bản dịch hệ thống
    with st.expander("👁 Xem bản dịch của hệ thống?"):
        st.info(st.session_state.model_translation)
