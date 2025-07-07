import json
import pandas as pd
from datetime import datetime
import uuid
import random
import psycopg2
from databases.connection import get_connection

def get_user_flashcards(user_id: int) -> pd.DataFrame:
    """
    Lấy danh sách flashcards của người dùng từ PostgreSQL (Neon).
    
    Args:
        user_id (int): ID người dùng.

    Returns:
        pd.DataFrame: DataFrame chứa thông tin flashcards.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT test_id, name, status, score, date_updated
            FROM flashcards
            WHERE user_id = %s
            ORDER BY date_updated DESC
        """
        cur.execute(query, (user_id,))
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        df = pd.DataFrame(rows, columns=colnames)
        return df

    except Exception as e:
        print(f"[get_user_flashcards] Lỗi: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()
    

def create_flashcard(user_id: int, test_name: str, vocabs_json: str):
    """
    Creates a new test with the given parameters.
    Args:
        user_id (int): The ID of the user creating the test.
        test_name (str): The name of the test.
        vocab_json (str): A JSON string containing the list of vocabulary words for the test.
    """

    # init test_id, date_updated, status, score
    test_id = str(uuid.uuid4())
    date_updated = datetime.now()
    status = 'Chưa làm'
    score = 0.0

    # connect to the database and insert the new test
    conn = get_connection()
    c = conn.cursor()

    # check if the test name already exists for the user
    c.execute("SELECT * FROM flashcards WHERE user_id = %s AND name = %s", (user_id, test_name))
    existing_flashcard = c.fetchone()

    if existing_flashcard:
        conn.close()
        print(f"[LOG] Flashcard '{test_name}' already exists for user {user_id}.")
        return False, "Tên flashcard đã tồn tại. Vui lòng chọn tên khác."
    
    try:
        c.execute("""
            INSERT INTO flashcards (test_id, user_id, name, status, score, date_updated, vocabs)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (test_id, user_id, test_name, status, score, date_updated, vocabs_json))
    except psycopg2.IntegrityError as e:
        print(f"[LOG] Error creating flashcard: {e}")
        conn.close()
        return False, str(e)
    
    conn.commit()
    conn.close()    
    return True, test_id

def delete_flashcard(test_id: int):
    """
    Deletes a test by its ID.
    
    Args:
        test_id (int): The ID of the test to be deleted.
    """
    conn = get_connection()
    c = conn.cursor()
    try: 
        c.execute("DELETE FROM flashcards WHERE test_id = %s", (test_id,))
    except psycopg2.Error as e:
        print(f"[LOG] Error deleting flashcard: {e}")
        conn.close()
        return False, str(e)
    
    conn.commit()
    conn.close()
    return True, "Đã xóa flashcard thành công!"
    
def get_flashcard_test(test_id: str):
    """
    Get the details for a specific flashcard test
    
    Args:
        test_id (str): The ID of the test
        
    Returns:
        dict: Test details including words
    """
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT name, vocabs FROM flashcards WHERE test_id = %s", (test_id,))
        result = c.fetchone()
        conn.close()
        
        if result:
            test_name, vocabs_json = result["name"], result["vocabs"]
            return {
                "test_id": test_id,
                "name": test_name,
                "words": json.loads(vocabs_json)
            }
        return None
    except Exception as e:
        print(f"[LOG] Error getting flashcard test: {e}")
        conn.close()
        return None

def update_flashcard_score(test_id: str, score: float, user_id: str, flashcard_name: str):
    """
    Update the score for a flashcard test
    
    Args:
        test_id (str): The ID of the test
        score (float): The new score (percentage correct)
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = get_connection()
    c = conn.cursor()
    date_updated = datetime.now()
    status = 'Đã làm'
    history_id = str(uuid.uuid4())
    
    try:
        c.execute("""
            UPDATE flashcards 
            SET score = %s, status = %s, date_updated = %s
            WHERE test_id = %s
        """, (score, status, date_updated, test_id))

        c.execute("""
            INSERT INTO flashcard_history (history_id, user_id, flashcard_name, score, time_updated)
            VALUES (%s, %s, %s, %s, %s)
        """, (history_id, user_id, flashcard_name, score, date_updated))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[LOG] Error updating flashcard score: {e}")
        conn.close()
        return False
    
# lấy số lượng flashcard đã học/đang học và trả về dataframe
def get_flashcard_status_count(user_id: str) -> pd.DataFrame:
    """
    Trả về DataFrame gồm 2 cột: status, count – số lượng flashcard theo trạng thái.

    Args:
        user_id (str): ID người dùng.

    Returns:
        pd.DataFrame: Cột 'status' là str, 'count' là int.
    """
    conn = get_connection()
    c = conn.cursor()

    # Query: lấy số lượng flashcard theo trạng thái
    c.execute("""
        SELECT status, COUNT(*) AS count 
        FROM flashcards 
        WHERE user_id = %s 
        GROUP BY status
    """, (user_id,))

    rows = c.fetchall()
    conn.close()

    # Chuyển thành DataFrame
    df = pd.DataFrame(rows, columns=["status", "count"])
    return df

# lấy lịch sử điểm số flashcard của người dùng
def get_flashcard_hisrory(user_id: str) -> pd.DataFrame:
    """
    Trả về DataFrame gồm 3 cột: date_taken, score, flashcard_name – lịch sử điểm số flashcard.

    Args:
        user_id (str): ID người dùng.

    Returns:
        pd.DataFrame: Cột 'date_taken' là datetime, 'score' là int, 'flashcard_name' là str.
    """
    conn = get_connection()
    c = conn.cursor()

    # Query: lấy lịch sử điểm số flashcard
    c.execute("""
        SELECT flashcard_name, score, time_updated
        FROM flashcard_history 
        WHERE user_id = %s 
        ORDER BY time_updated DESC
    """, (user_id,))

    rows = c.fetchall()
    conn.close()

    # Chuyển thành DataFrame
    df = pd.DataFrame(rows, columns=["flashcard_name", "score", "time_updated"])
    return df