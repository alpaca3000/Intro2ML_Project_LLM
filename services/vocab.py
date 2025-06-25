import json
import psycopg2
import streamlit as st
import uuid
from datetime import datetime
from databases.connection import get_connection

# add new vocabulary to user's vocabulary list
def add_vocab(user_id: str, vocab: str, definition: str, word_class: str, examples: list, synonyms: str):
    """
    Adds a new vocabulary to the database.
    Args:
        user_id (str): The ID of the user adding the vocabulary.
        en (str): The English word.
        vi (str): The Vietnamese definition of the word.
        word_class (str): The class of the word (e.g., noun, verb).
        examples_en (str): An examples sentence in English using the word.
        synonyms (str):  A comma-separated string of synonyms for the word.
    """
    
    # init vocab_id and date_created
    vocab_id = str(uuid.uuid4())
    date_created = datetime.now().date().isoformat()
    status = "Đang học"
    examples_json = json.dumps(examples or [])
    
    # connect to the database
    conn = get_connection()
    c = conn.cursor()

    result = True
    message = vocab_id

    # check if this word already exists in the user's vocabulary by en and vi
    c.execute("SELECT * FROM vocabulary WHERE user_id = %s AND en = %s AND vi = %s", (user_id, vocab, definition))
    existing_vocab = c.fetchone()

    if existing_vocab:
        conn.close()
        result = False
        message = "Từ vựng đã tồn tại trong từ điển của bạn."
        print(f"[LOG] Vocabulary '{vocab}' already exists for user {user_id}.")
    else:
        # insert new vocabulary into the database
        try:
            c.execute("""
                INSERT INTO vocabulary (vocab_id, user_id, en, vi, class, examples, synonyms, status, date_added)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (vocab_id, user_id, vocab, definition, word_class, examples_json, synonyms, status, date_created))
        except Exception as e:
            message = e
            result = False
            print(f"[LOG] Error adding vocabulary: {e}")
        finally:
            conn.commit()
            conn.close()

    return result, message

# get all vocabulary of a user
st.cache_data(show_spinner=False)  # Cache the function for 1 hour
def get_user_vocabulary(user_id: str):
    """
    Retrieves all vocabulary for a specific user.
    
    Args:
        user_id (str): The ID of the user whose vocabulary is to be retrieved.
    
    Returns:
        list: A list of vocabulary entries for the user.
    """
    
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT vocab_id, en, vi, class, examples, synonyms, status, date_added FROM vocabulary WHERE user_id = %s", (user_id,))
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
    
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM vocabulary WHERE vocab_id = %s", (vocab_id,))
    except psycopg2.Error as e:
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
    
    conn = get_connection()
    c = conn.cursor()
    try: 
        c.execute("UPDATE vocabulary SET status = %s WHERE vocab_id = %s", (new_status, vocab_id))

    except psycopg2.Error as e:
        print(f"[LOG] Error updating vocabulary status: {e}")
        conn.close()
        return False, str(e)
    
    conn.commit()
    conn.close()
    
    # log to check if the vocabulary status was updated successfully
    print(f"[LOG] Vocabulary with ID {vocab_id} updated successfully to status '{new_status}'.")
    return True, "Cập nhật trạng thái từ vựng thành công!"

# # update a vocabulary's details by id
# def update_vocab(vocab_id: str, new_meaning, new_class, new_examples_en: str, new_examples_vi: str, new_status: str): 
#     """
#     Updates the meaning, examples sentences, and status of a vocabulary entry by its ID.
    
#     Args:
#         vocab_id (str): The ID of the vocabulary to be updated.
#         new_meaning (str): The new meaning of the vocabulary.
#         new_examples_en (str): The new examples sentence in English.
#         new_examples_vi (str): The new examples sentence in Vietnamese.
#         new_status (str): The new status of the vocabulary.
#     """
#     date_updated = datetime.now().date().isoformat()
    
#     conn = get_connection()
#     c = conn.cursor()
    
#     try:
#         c.execute("""
#             UPDATE vocabulary 
#             SET vi = %s, class = %s, examples_en = %s, examples_vi = %s, status = %s, date_added = %s 
#             WHERE vocab_id = %s
#         """, (new_meaning, new_class, new_examples_en, new_examples_vi, new_status,date_updated, vocab_id))
#     except Exception as e:
#         print(f"[LOG] Error updating vocabulary: {e}")
#         conn.close()
#         return False, str(e)
    
#     conn.commit()
#     conn.close()

#     # log to check if the vocabulary was updated successfully
#     print(f"[LOG] Vocabulary with ID {vocab_id} updated successfully.")

#     return True, "Cập nhật từ vựng thành công!"
    
