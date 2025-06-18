import sqlite3

def create_tables():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # create user table
    c.execute("""
              CREATE TABLE IF NOT EXISTS users (
              user_id TEXT PRIMARY KEY,
              username TEXT UNIQUE,
              password TEXT,
              email TEXT UNIQUE
              )
              """)
    
    # create vocabulary table
    c.execute("""
              CREATE TABLE IF NOT EXISTS vocabulary (
              vocab_id TEXT PRIMARY KEY,
              user_id TEXT,
              en TEXT,
              vi TEXT,
              class TEXT,
              example_en TEXT,
              example_vi TEXT,
              status TEXT DEFAULT 'studying',
              date_added TEXT DEFAULT (datetime('now')),
              FOREIGN KEY (user_id) REFERENCES users(user_id)
              )
              """)
    
    # create flashcards table
    c.execute("""
              CREATE TABLE IF NOT EXISTS flashcards (
              test_id TEXT PRIMARY KEY,  
              user_id TEXT,
              name TEXT,
              status TEXT DEFAULT 'chưa làm',
              score REAL DEFAULT 0.0,
              date_updated TEXT DEFAULT (datetime('now')),
              vocabs TEXT,
              FOREIGN KEY (user_id) REFERENCES users(user_id)       
              )
              """)

    # create evaluation table include user_id, average_score, total_translations
    c.execute("""
              CREATE TABLE IF NOT EXISTS evaluations (
              evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id TEXT,
              average_score REAL DEFAULT 0.0,
              total_translations INTEGER DEFAULT 0,
              FOREIGN KEY (user_id) REFERENCES users(user_id)
              )
              """)
    
    conn.commit()
    conn.close()

    # trong đó vocabs là một chuỗi JSON chứa danh sách các từ vựng trong bài test dưới dạng {"vocab_id": ..., "en": ..., "vi": ...}, 
    # có thể dùng json.dumps() để chuyển đổi danh sách thành chuỗi JSON khi lưu vào cơ sở dữ liệu và json.loads() để chuyển đổi ngược lại khi lấy ra.

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")