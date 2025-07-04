import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from services.vocab import get_user_vocabulary, delete_vocab, update_vocab_status
from services.translate import translate_text
from utils.session import is_logged_in
from components.feedback import confirm_modal, toast
from streamlit_modal import Modal
import uuid

# initialize session state for editing and deleting word
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None
if "deleting_id" not in st.session_state:
    st.session_state.deleting_id = None
if "grid_key_vocabulary" not in st.session_state:
    st.session_state.grid_key_vocabulary = "vocabulary_table"


# page title
st.title("TRANG TỪ VỰNG CỦA TÔI")

# check if user is logged in
if not is_logged_in():
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
    height=min(300, (len(vocabulary_df) + 2) * 32 + 32),
    key=st.session_state.grid_key_vocabulary
)

# get selected word
selected_row = vocabulary_table["selected_rows"]

status_modal = Modal("Cập nhật trạng thái", key="update_status_modal", max_width=500)
delete_modal = Modal("Xóa từ vựng", key="delete_vocab_modal", max_width=500)

def update_vocab_status_callback():
    """Callback function to update vocabulary status."""
    vocab_id = selected_row["vocab_id"].values[0]
    new_status = "Đã nhớ" if selected_row["status"].values[0] == "Đang học" else "Đang học"
    result, message = update_vocab_status(vocab_id, new_status)
    if result:
        st.session_state.grid_key_vocabulary = str(uuid.uuid4())
        st.editing_id = None
    return result, message

def delete_vocab_callback():
    """Callback function to delete vocabulary."""
    vocab_id = selected_row["vocab_id"].values[0]
    result, message = delete_vocab(vocab_id)
    if result:
        st.session_state.grid_key_vocabulary = str(uuid.uuid4())
        st.session_state.deleting_id = None
    return result, message

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
    else: 
        st.markdown("- **Ví dụ:** Không có ví dụ nào được cung cấp.")
    st.markdown(f"- **Từ đồng nghĩa:** {selected_row['synonyms'].values[0]}")

left_blank_col, col1, col2, right_blank_col = st.columns([1, 2, 2, 1])
with col1:
    if st.button("Cập nhật trạng thái", use_container_width=True, icon="⚠️", disabled=(selected_row is None)):
        st.session_state.editing_id = selected_row["vocab_id"].values[0]
        status_modal.open()   
        
with col2:
    if st.button("🗑️ Xóa từ", use_container_width=True, disabled=(selected_row is None)):
        st.session_state.deleting_id = selected_row["vocab_id"].values[0]
        delete_modal.open()

if status_modal.is_open() and st.session_state.editing_id is not None:
    st.session_state.editing_id = None
    current_status = selected_row["status"].values[0]
    new_status = "Đã nhớ" if current_status == "Đang học" else "Đang học"
    confirm_modal(status_modal, 
        message = (
            f"Xác nhận đổi trạng thái của <strong>{selected_row['en'].values[0]}</strong> "
            f"từ <strong>{current_status}</strong> thành <strong>{new_status}</strong> không?"
        ),
        confirm_label="✔️ Xác nhận",
        on_confirm_callback=update_vocab_status_callback,
        session_key="update_status_modal"
    )

toast("update_status_modal")

if delete_modal.is_open() and st.session_state.deleting_id is not None:
    st.session_state.deleting_id = None
    confirm_modal(delete_modal, 
        message=f"Xác nhận xóa <strong>{selected_row['en'].values[0]}</strong> khỏi từ điển?",
        confirm_label="✔️ Xác nhận",
        on_confirm_callback=delete_vocab_callback,
        session_key="delete_vocab_modal"
    )

toast("delete_vocab_modal")