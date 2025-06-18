# Envichan - English to Vietnamese Learning Platform

## 📖 Giới thiệu

Envichan là một ứng dụng học tiếng Anh trực tuyến xây dựng trên nền tảng Streamlit, cung cấp các công cụ dịch thuật tiếng Anh sang tiếng Việt, quản lý từ vựng cá nhân, hệ thống flashcard và đánh giá khả năng dịch thuật.

## 🚀 Tính năng chính

- **Dịch thuật**: Dịch văn bản từ tiếng Anh sang tiếng Việt sử dụng mô hình AI tiên tiến
- **Từ điển cá nhân**: Thêm, chỉnh sửa và quản lý danh sách từ vựng của bạn
- **Flashcard**: Tạo và luyện tập với các bộ thẻ flashcard từ từ vựng đã lưu
- **Đánh giá dịch thuật**: So sánh bản dịch của bạn với bản dịch của hệ thống
- **Quản lý tài khoản**: Hệ thống đăng ký, đăng nhập người dùng

## 🧠 Mô hình sử dụng

Envichan sử dụng mô hình dịch thuật được huấn luyện trước từ Hugging Face:

- **Mô hình dịch thuật**: `alpaca3000/en-vi-translation-model`
- **Framework**: PyTorch và Transformers
- **Caching**: Streamlit caching để tối ưu hiệu suất

## 🛠️ Cài đặt và sử dụng

### Yêu cầu hệ thống

- Python 3.8+
- SQLite

### Cài đặt

1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/Envichan.git
   cd Envichan
   ```

2. Cài đặt các thư viện cần thiết
   ```bash
   pip install -r requirement.txt
   ```

3. Khởi tạo cơ sở dữ liệu
   ```bash
   cd databases
   python init_db.py
   cd ..
   ```

4. Chạy ứng dụng
   ```bash
   streamlit run Home.py
   ``` 
   hoặc
   ```bash
   streamlit run Home.py --server.headless true
   ```

### Hướng dẫn sử dụng
1. Trang chủ:

- Dịch văn bản tiếng Anh sang tiếng Việt
- Thêm từ vựng mới vào từ điển cá nhân (yêu cầu đăng nhập)

2. Tài khoản của tôi:

- Đăng ký tài khoản mới
- Đăng nhập vào hệ thống

3. Từ điển của tôi:

- Xem danh sách từ vựng đã lưu
- Chỉnh sửa hoặc xóa từ vựng
- Flashcard của tôi:

4. Tạo bộ flashcard mới từ từ vựng đã lưu
- Luyện tập với các bộ flashcard

5. Đánh giá dịch thuật:

- Thực hành dịch văn bản và nhận đánh giá
- So sánh bản dịch của bạn với bản dịch của hệ thống

## Cấu trúc project

Envichan/
├── Home.py                   # Trang chủ
├── pages/                    # Các trang trong ứng dụng
│   ├── My_account.py         # Quản lý tài khoản
│   ├── My_dictionary.py      # Từ điển cá nhân
│   ├── My_flashcard.py       # Quản lý flashcard
│   └── Translate_evalution.py # Đánh giá dịch thuật
├── services/                 # Các dịch vụ của ứng dụng
│   ├── auth.py               # Xác thực người dùng
│   ├── flashcard.py          # Quản lý flashcard
│   ├── translate.py          # Dịch thuật
│   └── vocab.py              # Quản lý từ vựng
├── components/               # Thành phần UI
│   └── flashcard_ui.py       # Giao diện flashcard
├── databases/                # Cơ sở dữ liệu
│   ├── database.db           # File SQLite
│   └── init_db.py            # Khởi tạo DB
├── utils/                    # Tiện ích
│   ├── model_storage.py      # Lưu trữ mô hình
│   └── session.py            # Quản lý phiên
└── requirements.txt          # Thư viện cần thiết