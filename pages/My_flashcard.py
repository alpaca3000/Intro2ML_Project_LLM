import streamlit as st
import pandas as pd
import time
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from services.flashcard import *
from services.vocab import get_user_vocabulary
from components.flashcard_ui import do_flashcard
from utils.session import is_logged_in
from streamlit_modal import Modal
from components.feedback import confirm_modal, toast
import uuid

# initialize session state for creating flashcard and deleting flashcard
if "show_create_form" not in st.session_state:
    st.session_state.show_create_form = False
if "doing_flashcard" not in st.session_state:
    st.session_state.doing_flashcard = False
if "current_test_id" not in st.session_state:
    st.session_state.current_test_id = None
if "delete_flashcard" not in st.session_state:
    st.session_state.delete_flashcard = False
if "grid_key" not in st.session_state:
    st.session_state.grid_key = "flashcard_table"

# Check if we're in flashcard mode
if st.session_state.doing_flashcard and st.session_state.current_test_id:
    do_flashcard(st.session_state.current_test_id)
    st.sidebar.title(f"Xin chào {st.session_state.username}!")
    st.stop()

# page title
st.title("FLASHCARD CỦA TÔI")

# check if user is logged in
if not is_logged_in():
    st.warning("Bạn cần đăng nhập để thực hiện chức năng này.")
    st.stop()

st.sidebar.title(f"Xin chào {st.session_state.username}!")

## ------------------- USER'S TEST TABLE ------------------
st.subheader("Danh sách flashcard của tôi")
test_data = get_user_flashcards(st.session_state["user_id"])
test_columns = ["test_id", "user_id", "name", "status", "score", "date_updated", "vocabs"]
test_df = pd.DataFrame(test_data, columns=test_columns)

# Xây dựng cấu hình bảng
gb_test = GridOptionsBuilder.from_dataframe(test_df)
gb_test.configure_selection(selection_mode="single", use_checkbox=True)
gb_test.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
gb_test.configure_default_column(editable=False, resizable=True)
gb_test.configure_column("user_id", hide=True) 
gb_test.configure_column("vocabs", hide=True)
gb_test.configure_grid_options(rowHeight=32)
test_table = AgGrid(
    test_df,
    gridOptions=gb_test.build(),
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    fit_columns_on_grid_load=True,
    height=min(300, (len(test_df) + 2) * 32 + 32),
    key=st.session_state.grid_key 
)

selected_row = test_table["selected_rows"]

delete_flashcard_modal = Modal("Xóa flashcard", key="delete_flashcard_modal", max_width=500)

def delete_flashcard_callback():
    flashcard_id = selected_row["test_id"].values[0]
    result, message = delete_flashcard(flashcard_id)
    if result:
        st.session_state.grid_key = str(uuid.uuid4())
    return result, message

left_blank_col, create_col, doing_col, remove_col, right_blank_col = st.columns([0.3,1,1,1,0.3])

with create_col:
    if st.button("Tạo flashcard mới",use_container_width=True, icon="➕"):
        st.session_state.show_create_form = True
        st.session_state.grid_key = str(uuid.uuid4())
        
with doing_col:
    if st.button("Bắt đầu làm bài", disabled=(selected_row is None), use_container_width=True, icon="🚀"):
        st.session_state.doing_flashcard = True
        st.session_state.current_test_id = selected_row["test_id"].values[0]
        st.rerun()

with remove_col:
    if st.button("Xóa flashcard", disabled=(selected_row is None), use_container_width=True, icon="🗑️"):
        st.session_state.delete_flashcard = True
        delete_flashcard_modal.open()

if delete_flashcard_modal.is_open() and st.session_state.delete_flashcard:
    st.session_state.delete_flashcard = False
    flashcard_name = selected_row["name"].values[0]
    confirm_modal(
        modal=delete_flashcard_modal,
        message=f"Xác nhận xóa flashcard <strong>{flashcard_name}</strong>?",
        confirm_label="✔️ Xác nhận",
        on_confirm_callback=delete_flashcard_callback,
        session_key="delete_flashcard_modal"
    )

    
toast("delete_flashcard_modal")
    
# if create flashcard button is clicked, show create form
if st.session_state.show_create_form:
    st.markdown("### 📚 Tạo bộ đề mới")
    with st.form("create_flashcard_form"):
        flashcard_name = st.text_input("Tên bộ đề", placeholder="Nhập tên bộ đề mới")

        data = get_user_vocabulary(st.session_state["user_id"])
        columns = ["vocab_id", "user_id", "en", "vi", "class", "example_en", "example_vi", "status", "date_added"]
        vocabulary_df = pd.DataFrame(data, columns=columns)
        
        # 2. Tạo label dễ hiểu: "fine - tốt", "fine - khỏe"
        label_map = {f"{row['en']} - {row['vi']}": row['vocab_id'] for _, row in vocabulary_df.iterrows()}

        # 3. Cho người dùng chọn nhiều từ
        selected_labels = st.multiselect("Chọn từ cho bộ đề:", options=list(label_map.keys()))

        # 4. Lấy vocab_id tương ứng
        selected_ids = [label_map[label] for label in selected_labels]

        # 5. Lấy dòng từ điển tương ứng
        selected_rows = vocabulary_df[vocabulary_df["vocab_id"].isin(selected_ids)]

        left_blank_col2, col_submitted, col_cancel, right_blank_col2 = st.columns([1, 1, 1, 1])
        with col_submitted:
            submitted = st.form_submit_button("Lưu thay đổi", use_container_width=True, icon="💾")
        with col_cancel:
            cancel = st.form_submit_button("Hủy", use_container_width=True, icon="❌")

        if submitted:
            if not flashcard_name:
                st.warning("Bạn cần nhập tên bộ đề.")
            elif selected_rows is not None:
                vocabs_json = selected_rows[["vocab_id", "en", "vi"]].to_json(orient="records")
                result, message = create_flashcard(st.session_state.user_id, flashcard_name, vocabs_json)
                if result:
                    st.toast("Đã tạo bộ đề thành công!", icon="✅")
                    st.session_state.show_create_form = False
                    time.sleep(1)
                    st.rerun()
                else:
                    st.toast(f"Lỗi: {message}", icon="❌")
            else:
                st.warning("Bạn cần chọn ít nhất một từ để tạo bộ đề.")

        if cancel:
            st.session_state.show_create_form = False
            st.rerun()