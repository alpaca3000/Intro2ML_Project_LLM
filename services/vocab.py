import sqlite3
import uuid
from datetime import datetime

# add new vocabulary to user's vocabulary list
def add_vocab(user_id: str, en: str, vi: str, word_class: str, example_en: str, example_vi: str, status: str = "Đang học"):
    """
    Adds a new vocabulary to the database.
    Args:
        user_id (str): The ID of the user adding the vocabulary.
        en (str): The English word.
        vi (str): The Vietnamese meaning of the word.
        word_class (str): The class of the word (e.g., noun, verb).
        example_en (str): An example sentence in English using the word.
        example_vi (str): An example sentence in Vietnamese using the word.
        status (str): The status of the vocabulary (e.g., "learning", "remembered").
    """
    
    # init vocab_id and date_created
    vocab_id = str(uuid.uuid4())
    date_created = datetime.now().date().isoformat()
    
    # connect to the database
    conn = sqlite3.connect("databases/database.db")
    c = conn.cursor()

    result = True
    message = vocab_id

    # check if this word already exists in the user's vocabulary by en and vi
    c.execute("SELECT * FROM vocabulary WHERE user_id = ? AND en = ? AND vi = ?", (user_id, en, vi))
    existing_vocab = c.fetchone()

    if existing_vocab:
        conn.close()
        result = False
        message = "Từ vựng đã tồn tại trong từ điển của bạn."
        print(f"[LOG] Vocabulary '{en}' already exists for user {user_id}.")
    else:
        # insert new vocabulary into the database
        try:
            c.execute("""
                INSERT INTO vocabulary (vocab_id, user_id, en, vi, class, example_en, example_vi, status, date_added)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (vocab_id, user_id, en, vi, word_class, example_en, example_vi, status, date_created))
        except sqlite3.IntegrityError as e:
            message = e
            result = False
            print(f"[LOG] Error adding vocabulary: {e}")
        finally:
            conn.commit()
            conn.close()

    return result, message

# get all vocabulary of a user
def get_user_vocabulary(user_id: str):
    """
    Retrieves all vocabulary for a specific user.
    
    Args:
        user_id (str): The ID of the user whose vocabulary is to be retrieved.
    
    Returns:
        list: A list of vocabulary entries for the user.
    """
    
    conn = sqlite3.connect("databases/database.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM vocabulary WHERE user_id = ?", (user_id,))
    results = c.fetchall()
    
    conn.close()
    
    return results

# delete a vocabulary by its ID
def delete_vocab(vocab_id: str):
    """
    Deletes a vocabulary entry by its ID.
    
    Args:
        vocab_id (str): The ID of the vocabulary to be deleted.
    """
    
    conn = sqlite3.connect("databases/database.db")
    c = conn.cursor()
    try:
        c.execute("DELETE FROM vocabulary WHERE vocab_id = ?", (vocab_id,))
    except sqlite3.Error as e:
        print(f"[LOG] Error deleting vocabulary: {e}")
        conn.close()
        return False, str(e)
    
    conn.commit()
    conn.close()
    
    # log to check if the vocabulary was deleted successfully
    print(f"[LOG] Vocabulary with ID {vocab_id} deleted successfully.")
    return True, "Xoá từ vựng thành công!"

# update a vocabulary's status by id
def update_vocab_status(vocab_id: str, new_status: str):
    """
    Updates the status of a vocabulary entry by its ID.
    
    Args:
        vocab_id (str): The ID of the vocabulary to be updated.
        status (str): The new status to set for the vocabulary.
    """
    
    conn = sqlite3.connect("databases/database.db")
    c = conn.cursor()
    
    c.execute("UPDATE vocabulary SET status = ? WHERE vocab_id = ?", (new_status, vocab_id))
    
    conn.commit()
    conn.close()
    
    # log to check if the vocabulary status was updated successfully
    print(f"[LOG] Vocabulary with ID {vocab_id} updated successfully to status '{new_status}'.")

# update a vocabulary's details by id
def update_vocab(vocab_id: str, new_meaning, new_class, new_example_en: str, new_example_vi: str, new_status: str): 
    """
    Updates the meaning, example sentences, and status of a vocabulary entry by its ID.
    
    Args:
        vocab_id (str): The ID of the vocabulary to be updated.
        new_meaning (str): The new meaning of the vocabulary.
        new_example_en (str): The new example sentence in English.
        new_example_vi (str): The new example sentence in Vietnamese.
        new_status (str): The new status of the vocabulary.
    """
    date_updated = datetime.now().date().isoformat()
    
    conn = sqlite3.connect("databases/database.db")
    c = conn.cursor()
    
    try:
        c.execute("""
            UPDATE vocabulary 
            SET vi = ?, class = ?, example_en = ?, example_vi = ?, status = ?, date_added = ? 
            WHERE vocab_id = ?
        """, (new_meaning, new_class, new_example_en, new_example_vi, new_status,date_updated, vocab_id))
    except sqlite3.IntegrityError as e:
        print(f"[LOG] Error updating vocabulary: {e}")
        conn.close()
        return False, str(e)
    
    conn.commit()
    conn.close()

    # log to check if the vocabulary was updated successfully
    print(f"[LOG] Vocabulary with ID {vocab_id} updated successfully.")

    return True, "Cập nhật từ vựng thành công!"
    
