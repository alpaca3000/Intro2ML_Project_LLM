import uuid
from psycopg2 import Error
from utils.password import hash_password, verify_password
from databases.connection import get_connection

def add_user_to_db(conn, username: str, hashed_password: str, email: str) -> bool:
    """
    Adds a new user to the database.
    
    Args:
        conn (sqlite3.Connection): The connection object to the database.
        username (str): The username of the new user.
        hashed_password (str): The hashed password of the new user.
        email (str): The email of the new user.
    
    Returns:
        bool: True if the user was added successfully, False otherwise.
    """
    user_id = str(uuid.uuid4())
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (user_id, username, password, email)
                VALUES (%s, %s, %s, %s)
            """, (user_id, username, hashed_password, email))
        return True
    except Exception as e:
        print(f"[ERROR] Failed to add user: {e}")
        return False

def register_user(username: str, password: str, email: str) -> str:
    """
    Register a new user with the given username, password, and email.
    
    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        email (str): The email of the user.
    
    Returns:
        bool: True if registration is successful, False otherwise.
    """

    conn = get_connection()
    message = ""
    result = False

    try:
        with conn.cursor() as cur:
            # Kiểm tra username
            cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
            if cur.fetchone():
                message = "Tên người dùng đã tồn tại! Vui lòng chọn tên khác."
                return False, message

            # Kiểm tra email
            cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                message = "Email đã được sử dụng! Vui lòng sử dụng email khác."
                return False, message

            # Hash password và thêm vào DB
            hashed_password = hash_password(password)
            if add_user_to_db(conn, username, hashed_password, email):
                conn.commit()
                result = True
                message = "success"
            else:
                message = "Không thể thêm người dùng vào cơ sở dữ liệu."

    except Error as e:
        message = f"Lỗi khi đăng ký người dùng: {e}"
        print(f"[ERROR] {message}")
    finally:
        conn.close()

    return result, message

def login_user(username: str, password: str):
    """
    Attempts to log in a user.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        Tuple[bool, str | None, str | None]:
            - success (bool): True if login successful, else False.
            - result (str | None): user_id if success, else error message.
    """
    conn = get_connection()
    c = conn.cursor()

    # Kiểm tra tồn tại username
    c.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
    row = c.fetchone()
    conn.close()
    result = False
    message = ""

    if row is None:
        message = "Tên người dùng không tồn tại."
    
    user_id_db, password_db = row["user_id"], row["password"]

    if not verify_password(password, password_db):
        message = f"Mật khẩu không đúng: {repr(password_db)}"
    else:
        result = True
        message = user_id_db

    return result, message