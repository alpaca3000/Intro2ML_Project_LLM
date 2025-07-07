import os
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# Đọc connection string từ biến môi trường
DATABASE_URL = os.getenv("DATABASE_URL")

# @st.cache_resource
def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        print(f"[ERROR] Không thể kết nối tới cơ sở dữ liệu: {e}")
        raise
