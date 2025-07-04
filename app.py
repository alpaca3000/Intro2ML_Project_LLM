import streamlit as st

pages = {
    "Trang chủ": [
        st.Page("pages/Home.py", title="Trang chủ", icon=":material/home:"),
    ],
    "Tài khoản": [
        st.Page("pages/My_account.py", title="Tài khoản của tôi", icon=":material/account_circle:"),
        #st.Page("pages/Dashboard.py", title="Dashboard", icon=":material/space_dashboard:"),
    ],
    "Tiện ích": [
        st.Page("pages/My_dictionary.py", title="Từ điển của tôi", icon=":material/book:"),
        st.Page("pages/My_flashcard.py", title="Flashcard của tôi", icon=":material/style:"),
        st.Page("pages/Translate_evalution.py", title="Đánh giá dịch thuật", icon=":material/grade:"),
    ],
}

pg = st.navigation(pages)
pg.run()