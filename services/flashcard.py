import json
import pandas as pd
from datetime import datetime
import uuid
import sqlite3
import random

def get_user_flashcards(user_id: int):
    """
    Retrieves all tests created by a specific user.
    
    Args:
        user_id (int): The ID of the user whose tests are to be retrieved.
    
    Returns:
        list: A list of tests created by the user.
    """
    try:
        conn = sqlite3.connect("databases/database.db")
        df = pd.read_sql_query(
            """
            SELECT test_id, name, status, score, date_updated
            FROM flashcards
            WHERE user_id = ?
            ORDER BY date_updated DESC
            """,
            conn,
            params=(user_id,)
        )
        conn.close()
        return df
    except Exception as e:
        print("Lỗi khi truy vấn flashcards:", e)
        return pd.DataFrame()
    

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
    date_updated = datetime.now().date().isoformat()
    status = 'chưa làm'
    score = 0.0

    # connect to the database and insert the new test
    conn = sqlite3.connect("databases/database.db")
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO flashcards (test_id, user_id, name, status, score, date_updated, vocabs)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (test_id, user_id, test_name, status, score, date_updated, vocabs_json))
    except sqlite3.IntegrityError as e:
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
    conn = sqlite3.connect("databases/database.db")
    c = conn.cursor()
    try: 
        c.execute("DELETE FROM flashcards WHERE test_id = ?", (test_id,))
    except sqlite3.Error as e:
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
    conn = sqlite3.connect("databases/database.db")
    c = conn.cursor()
    try:
        c.execute("SELECT name, vocabs FROM flashcards WHERE test_id = ?", (test_id,))
        result = c.fetchone()
        conn.close()
        
        if result:
            test_name, vocabs_json = result
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

def update_flashcard_score(test_id: str, score: float):
    """
    Update the score for a flashcard test
    
    Args:
        test_id (str): The ID of the test
        score (float): The new score (percentage correct)
        
    Returns:
        bool: True if successful, False otherwise
    """
    conn = sqlite3.connect("databases/database.db")
    c = conn.cursor()
    date_updated = datetime.now().date().isoformat()
    status = 'đã làm'
    
    try:
        c.execute("""
            UPDATE flashcards 
            SET score = ?, status = ?, date_updated = ?
            WHERE test_id = ?
        """, (score, status, date_updated, test_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[LOG] Error updating flashcard score: {e}")
        conn.close()
        return False
    
