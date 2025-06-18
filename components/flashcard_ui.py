import streamlit as st
import streamlit.components.v1 as components
import os
import random
from services.flashcard import get_flashcard_test, update_flashcard_score

def do_flashcard(test_id):
    """Display and manage the flashcard UI for a given test"""
    # Track the current test_id to handle test switching properly
    if "current_test_id" not in st.session_state or st.session_state.current_test_id != test_id:
        # Reset all flashcard-related state when loading a new test
        reset_flashcard_state()
        st.session_state.current_test_id = test_id
    
    # Get test details
    test = get_flashcard_test(test_id)
    if not test:
        st.error("Không tìm thấy đề thi!")
        return
    
    # Initialize session state for flashcards (only if not already set)
    if "flashcard_index" not in st.session_state:
        st.session_state.flashcard_index = 0
    if "remembered_count" not in st.session_state:
        st.session_state.remembered_count = 0
    if "completed" not in st.session_state:
        st.session_state.completed = False
    if "words" not in st.session_state or st.session_state.words is None:
        st.session_state.words = test["words"]
        st.session_state.original_words = test["words"].copy()  # Keep original order
    
    words = st.session_state.words
    total_words = len(words)
    
    # Safety check to prevent division by zero
    if total_words == 0:
        st.error("Không tìm thấy từ vựng trong bài test này!")
        if st.button("Quay lại danh sách"):
            reset_flashcard_state()
            st.session_state.doing_flashcard = False
            st.rerun()
        return
    
    # Display test name and progress
    st.title(f"Flashcard: {test['name']}")
    
    # If we've gone through all words, show completion screen
    if st.session_state.flashcard_index >= total_words:
        st.session_state.completed = True
    
    if st.session_state.completed:
        # Calculate and save score
        score = (st.session_state.remembered_count / total_words) * 100
        update_flashcard_score(test_id, score)
        
        st.success(f"Hoàn thành! Bạn đã ghi nhớ {st.session_state.remembered_count}/{total_words} từ ({score:.1f}%)")
        
        # Buttons to restart or returnfg
        pass_col, blank_1, blank_2, fail_col = st.columns([1.5,1,1,1])
        with fail_col:
            if st.button("Làm lại", key="restart_button", use_container_width=True, icon="🔄"):
                st.session_state.flashcard_index = 0
                st.session_state.remembered_count = 0
                st.session_state.completed = False
                st.session_state.words = st.session_state.original_words.copy()  # Reset to original order
                st.rerun()
        with pass_col:
            if st.button("Quay lại danh sách", key="back_button", use_container_width=True, icon="🔙"): # icon danh sách
                reset_flashcard_state()  # Use helper function to reset state
                st.session_state.doing_flashcard = False
                st.rerun()
    else:
        back_col1, blank_3, blank_4, shuffle_col  = st.columns([1.5, 1, 1, 1])
        with shuffle_col:
            if st.button("TRỘN THẺ", key="shuffle_button", disabled=(st.session_state.flashcard_index != 0), use_container_width=True, icon="🔀"):
                shuffled = st.session_state.words.copy()
                random.shuffle(shuffled)
                st.session_state.words = shuffled
                st.rerun()
        with back_col1:
            if st.button("Quay lại danh sách", key="back_button", use_container_width=True, icon="🔙"):  # icon danh sách
                reset_flashcard_state()  # Use helper function to reset state
                st.session_state.doing_flashcard = False
                st.rerun()

        # Show progress and shuffle button
        progress = st.session_state.flashcard_index / total_words
        
        st.progress(progress)
        st.write(f"Tiến độ: {st.session_state.flashcard_index + 1}/{total_words}")
        
        # Get current word
        current_word = words[st.session_state.flashcard_index]
        
        # Display flashcard using components.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "index.html")
        
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Replace placeholders with actual content
        html_content = html_content.replace("__FRONT__", current_word["en"])
        html_content = html_content.replace("__BACK__", current_word["vi"])
        
        # Display the component
        components.html(html_content, height=270)
        
        # Add buttons for navigation using Streamlit
        left_blank_col, pass_col, fail_col, right_blank_col = st.columns([1,1,1,1])
        with pass_col:
            if st.button("✔", key=f"remembered_{st.session_state.flashcard_index}", use_container_width=True):
                st.session_state.remembered_count += 1
                st.session_state.flashcard_index += 1
                st.rerun()
        with fail_col:
            if st.button("✖", key=f"learning_{st.session_state.flashcard_index}", use_container_width=True):
                st.session_state.flashcard_index += 1
                st.rerun()

        


def reset_flashcard_state():
    """Helper function to completely reset all flashcard-related state"""
    # List of all keys related to flashcard functionality
    flashcard_keys = [
        "flashcard_index", 
        "remembered_count", 
        "completed", 
        "words", 
        "original_words"
    ]
    
    # Delete keys from session_state if they exist
    for key in flashcard_keys:
        if key in st.session_state:
            del st.session_state[key]