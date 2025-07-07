import nltk
import os

# Tự động thêm đường dẫn nltk_data vào nltk
nltk_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)