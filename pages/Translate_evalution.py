import streamlit as st
from transformers import MarianTokenizer, MarianMTModel
from nltk.corpus import wordnet
import nltk
from services.translate import save_translation_history, evaluate_translation
from utils.session import is_logged_in

# Tải dữ liệu WordNet (chỉ chạy lần đầu)
nltk.download('wordnet')
nltk.download('punkt')

# Đường dẫn đến mô hình trong thư mục Downloads
import os
MODEL_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "my_en_vi_translation_model_archive")  
# Tải mô hình (cache để tăng tốc)
@st.cache_resource
def load_model():
    try:
        tokenizer = MarianTokenizer.from_pretrained(MODEL_PATH)
        model = MarianMTModel.from_pretrained(MODEL_PATH)
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model: {e}. Please ensure the model files are in {MODEL_PATH}.")
        st.stop()

# Hàm dịch máy (để dùng trực tiếp nếu cần)
def machine_translate(sentence, tokenizer, model):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# Hàm lấy thông tin từ WordNet (nếu là từ đơn)
def get_wordnet_info(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return None
    synset = synsets[0]  # Lấy synset đầu tiên
    return {
        "definition": synset.definition(),
        "examples": synsets[0].examples(),
        "synonyms": [lemma.name() for lemma in synset.lemmas()],
        "pos": synset.pos()
    }

# Khởi tạo biến session
for key in ["percentage_correct", "model_translation", "show_result", "comparison"]:
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

# Kiểm tra xem văn bản có phải là từ đơn để thêm WordNet
if len(english_text.split()) == 1:  # Nếu là từ đơn
    wordnet_info = get_wordnet_info(english_text)
    if wordnet_info:
        with st.expander("Thông tin từ điển (WordNet)"):
            st.write(f"**Định nghĩa (English):** {wordnet_info['definition']}")
            st.write(f"**Ví dụ (English):** {wordnet_info['examples']}")
            st.write(f"**Từ đồng nghĩa (English):** {wordnet_info['synonyms']}")

# Nếu chưa có kết quả, cho nhập bản dịch
if not st.session_state.show_result:
    user_input = st.text_area("Nhập bản dịch của bạn:")

    blank_col, eval_col = st.columns([3, 1])
    with eval_col:
        if st.button("Đánh giá", use_container_width=True, icon="🔍"):
            if not user_input.strip():
                st.warning("⚠️ Vui lòng nhập bản dịch.")
            else:
                percent, translation, comparison = evaluate_translation(english_text, user_input)
                st.session_state.percentage_correct = percent
                st.session_state.model_translation = translation
                st.session_state.comparison = comparison
                st.session_state.show_result = True
                # Lưu lịch sử
                save_translation_history(st.session_state["user_id"], english_text, user_input, translation, percent)

# Kết quả sau khi đánh giá
if st.session_state.show_result:
    percent = st.session_state.percentage_correct
    if percent >= 80:
        st.success(f"✅ Bản dịch của bạn chính xác {percent:.2f}%")
    else:
        st.error(f"🚫 Bản dịch của bạn chỉ chính xác {percent:.2f}%.")

    st.write(f"**So sánh:** {st.session_state.comparison}")

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
