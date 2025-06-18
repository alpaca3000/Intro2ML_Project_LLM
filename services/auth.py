import uuid
import sqlite3

def get_connection():
    """
    Establishes a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: A connection object to the database.
    """
    return sqlite3.connect("databases/database.db")

def check_user_exists(conn, username: str) -> bool:
    """
    Checks if a user with the given username exists in the database.
    
    Args:
        conn (sqlite3.Connection): The connection object to the database.
        username (str): The username to check.
    
    Returns:
        bool: True if the user exists, False otherwise.
    """
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    username = c.fetchone()
    return username is not None

def check_email_exists(conn, email: str) -> bool:
    """
    Checks if an email already exists in the database.
    
    Args:
        conn (sqlite3.Connection): The connection object to the database.
        email (str): The email to check.
    
    Returns:
        bool: True if the email exists, False otherwise.
    """
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    email = c.fetchone()
    return email is not None

def add_user_to_db(conn, username: str, password: str, email: str) -> bool:
    """
    Adds a new user to the database.
    
    Args:
        conn (sqlite3.Connection): The connection object to the database.
        username (str): The username of the new user.
        password (str): The password of the new user.
        email (str): The email of the new user.
    
    Returns:
        bool: True if the user was added successfully, False otherwise.
    """
    user_id = str(uuid.uuid4())
    
    try:
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (user_id, username, password, email)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, password, email))
        return True
    except sqlite3.IntegrityError as e:
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
    # Placeholder for actual registration logic
    # kiểm tra tên người dùng đã tồn tại, nếu đã tồn tại thì tra
    conn = get_connection()
    message = ""
    result = False

    try: 
        if check_user_exists(conn, username):
            message = "Tên người dùng đã tồn tại! Vui lòng chọn tên khác."
        elif check_email_exists(conn, email):
            message = "Email đã được sử dụng! Vui lòng sử dụng email khác."
        else:
            add_user_to_db(conn, username, password, email)
            conn.commit()
            message = "susscess"
            result = True
    except sqlite3.Error as e:
        message = f"Lỗi khi đăng ký người dùng: {e}"
        print(f"[ERROR] {message}")
    finally:
        conn.close()

    return result, message

# def login_user(username: str, password: str) -> bool:
#     """
#     Log in a user with the given username and password.
    
#     Args:
#         username (str): The username of the user.
#         password (str): The password of the user.
    
#     Returns:
#         bool: True if login is successful, False otherwise.
#     """
#     # Placeholder for actual login logic
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute("SELECT password FROM users WHERE username = ?", (username,))
#     result = c.fetchone()
#     conn.close()
#     if result is None or result[0] != password:
#         return False  # Invalid username or password
#     # If the password matches, login is successful
#     print(f"[LOG] User {username} logged in successfully.")
#     return True

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
    c.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    result = False
    message = ""

    if row is None:
        message = "Tên người dùng không tồn tại."
    
    user_id_db, password_db = row

    if password != password_db:
        message = "Mật khẩu không đúng."
    else:
        result = True
        message = user_id_db

    return result, message