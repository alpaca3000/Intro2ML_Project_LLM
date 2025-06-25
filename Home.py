import streamlit as st
from services.translate import translate_text
from services.vocab import add_vocab
from utils.session import is_logged_in
from services.translate import load_translation_model
from services.word_info import get_word_info

tokenizer, model = load_translation_model()

# Giới thiệu về trang web envichan
st.title("Chào mừng đến với Envichan!")
st.write("Envichan là một ứng dụng học tiếng Anh trực tuyến, nơi bạn có thể học từ vựng, ngữ pháp và thực hành giao tiếp.")

# Hiển thị phần dịch tiếng Anh sang tiếng Việt
st.subheader("Dịch tiếng Anh sang tiếng Việt")
text = st.text_area("Nhập nội dung tiếng Anh:")
blank_col, translate_col = st.columns([4, 1])
with translate_col:
    translate = st.button("Dịch", use_container_width=True)
        
if translate: 
    result = translate_text(text)
    st.success(result)

# Hiển thị phần tra cứu từ vựng mới
st.subheader("Phát hiện từ vựng mới ? Tra cứu ngay!")
word_to_lookup = st.text_input("Nhập từ tiếng Anh cần tra cứu:", key="word_lookup_input", placeholder="Ví dụ: friendly, beautiful, etc.")

if word_to_lookup:
    word_info = get_word_info(word_to_lookup)
    if word_info:
        st.write(f"Kết quả tra cứu cho: **{word_to_lookup}**")
        for idx, info in enumerate(word_info):
            part_of_speech = info.get('part_of_speech', 'Không rõ')
            definition = info['definition']
            examples = info.get('examples', [])
            synonyms = ', '.join(info['synonyms']) if info.get('synonyms') else 'Không có từ đồng nghĩa'

            with st.expander(f"Định nghĩa {idx+1}: {info['definition']}"):
                st.markdown(f"**Loại từ:** `{part_of_speech}`")                
                
                st.markdown(f"**Định nghĩa:** {definition}")

                if info.get('examples'):
                    st.markdown("**Ví dụ:**")
                    for example in info['examples']:
                        st.markdown(f"- _{example}_")

                st.markdown(f"**Từ đồng nghĩa:** {synonyms}")

                if st.button(f"➕ Thêm định nghĩa {idx+1} vào từ điển", key=f"add_def_{idx}", use_container_width=True):
                    # check xem người dùng đã đăng nhập chưa
                    if not is_logged_in():
                        st.warning("Bạn cần đăng nhập để thực hiện chức năng này.")
                        
                    else:
                        user_id = st.session_state.get("user_id")
                        result, message = add_vocab(user_id, word_to_lookup, definition, part_of_speech, examples, synonyms)
                        if result:
                            st.toast(f"✅ Đã thêm từ vựng '{word_to_lookup}' vào từ điển của bạn!")
                        else: 
                            st.error(f"❌ Lỗi: {message}")
    else:
        st.error("Không tìm thấy thông tin cho từ này. Vui lòng thử lại với từ khác.")