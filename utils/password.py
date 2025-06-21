import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # lưu chuỗi này vào DB

def verify_password(password: str, hashed_password_from_db: str) -> bool:
    print("Từ DB:", repr(hashed_password_from_db))
    print("Độ dài:", len(hashed_password_from_db))
    print("Loại:", type(hashed_password_from_db))
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8'))
