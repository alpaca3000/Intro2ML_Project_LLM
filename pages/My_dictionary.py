import streamlit as st
import pandas as pd
import time
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from services.vocab import get_user_vocabulary, delete_vocab, update_vocab_status
from services.translate import translate_text
from utils.session import is_logged_in

# initialize session state for editing and deleting word
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None
if "deleting_id" not in st.session_state:
    st.session_state.deleting_id = None


# page title
st.title("TRANG TỪ VỰNG CỦA TÔI")

# check if user is logged in
if "is_logged_in" not in st.session_state or not st.session_state.is_logged_in:
    st.warning("Bạn cần đăng nhập để thực hiện chức năng này.")
    st.stop()

st.sidebar.title(f"Xin chào {st.session_state.username}!")

## ------------------- USER VOCABULARY TABLE ------------------
st.subheader("Danh sách từ vựng của tôi")

data = get_user_vocabulary(st.session_state["user_id"])
columns = ["vocab_id", "user_id", "en", "vi", "class", "examples", "synonyms", "status", "date_added"]
vocabulary_df = pd.DataFrame(data, columns=columns)

# Xây dựng cấu hình bảng
gb_vocabulary = GridOptionsBuilder.from_dataframe(vocabulary_df)
gb_vocabulary.configure_selection(selection_mode="single", use_checkbox=True)
gb_vocabulary.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
gb_vocabulary.configure_default_column(editable=False, resizable=True)
gb_vocabulary.configure_column("user_id", hide=True)  # Ẩn cột user_id
gb_vocabulary.configure_column("synonyms", hide=True)  # Ẩn cột synonyms
# gb_vocabulary.configure_column("date_added", hide=True)  # Ẩn cột vocab_id
gb_vocabulary.configure_column("examples", hide=True)  # Ẩn cột examples
gb_vocabulary.configure_grid_options(rowHeight=32)
vocabulary_table = AgGrid(
    vocabulary_df,
    gridOptions=gb_vocabulary.build(),
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    fit_columns_on_grid_load=True,
    height=min(300, (len(vocabulary_df) + 2) * 32 + 32)
)

# get selected word
selected_row = vocabulary_table["selected_rows"]

# when 1 row is selected, show edit and delete buttons
if selected_row is not None:
    # Hiển thị thông tin chi tiết từ
    st.markdown(f"### Từ vựng: **{selected_row['en'].values[0]}**")
    st.markdown(f"- **Định nghĩa:** {selected_row['vi'].values[0]}")
    st.markdown(f"- **Loại từ:** {selected_row['class'].values[0]}")
    examples = selected_row["examples"].values[0]
    if examples:
        st.markdown(f"- **Ví dụ:**")
        blank_col, example_col = st.columns([1, 9])
        with example_col:
            for idx, example in enumerate(examples):
                with st.expander(f"- **{example}**"):
                    st.write(f"Tạm dịch: {translate_text(example)}")
        # for example in examples:
        #     st.markdown(f"  - **{example}**")

    else: 
        st.markdown("- **Ví dụ:** Không có ví dụ nào được cung cấp.")
    st.markdown(f"- **Từ đồng nghĩa:** {selected_row['synonyms'].values[0]}")

left_blank_col, col1, col2, right_blank_col = st.columns([1, 2, 2, 1])
with col1:
    if st.button("Cập nhật trạng thái", use_container_width=True, icon="✏️", disabled=(selected_row is None)):
        st.session_state.editing_id = selected_row["vocab_id"].values[0]
with col2:
    if st.button("Xóa", use_container_width=True, icon="🗑️", disabled=(selected_row is None)):
        st.session_state.deleting_id = selected_row["vocab_id"].values[0]

# Nếu đang chỉnh sửa
if st.session_state.editing_id is not None:
    # Lấy trạng thái hiện tại
    current_status = selected_row["status"].values[0]
    new_status = "Đã nhớ" if current_status == "Đang học" else "Đang học"

    st.warning(f"⚠️ Xác nhận đổi từ **{current_status}** → **{new_status}** ? ")

    left_blank_col, col_confirm, col_cancel, right_blank_col = st.columns([1, 1, 1, 1])
    with col_confirm:
        if st.button("✔️ Xác nhận", use_container_width=True):
            result, message = update_vocab_status(st.session_state.editing_id, new_status)
            if result:
                st.toast(f"✅ Cập nhật trạng thái từ vựng thành công!")
            else:
                st.error(f"❌ Lỗi: {message}")
            st.session_state.editing_id = None
            time.sleep(1)
            st.rerun()

    with col_cancel:
        if st.button("❌ Hủy", use_container_width=True):
            st.session_state.editing_id = None
            st.rerun()

# Nếu đang xóa
if st.session_state.deleting_id is not None:
    st.warning("⚠️ Bạn có chắc muốn xóa từ này? Hành động này không thể hoàn tác.")

    left_blank_col1, col_confirm, col_cancel, right_blank_col1 = st.columns([1, 1, 1, 1])
    with col_confirm:
        if st.button("Xác nhận xóa", use_container_width=True, icon="✅"):
            result, message = delete_vocab(selected_row["vocab_id"].values[0])
            if result:
                st.toast("Đã xóa từ vựng thành công!", icon="🗑️")
            else:
                st.error(f"❌ Lỗi: {message}")
            st.session_state.deleting_id = None
            time.sleep(1)
            st.rerun()

    with col_cancel:
        if st.button("Hủy", use_container_width=True, icon="❌"):
            st.session_state.deleting_id = None
            st.rerun()