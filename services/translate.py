from transformers import MarianTokenizer, MarianMTModel
import torch
import streamlit as st
from sacrebleu import sentence_bleu
import os

@st.cache_resource
def load_translation_model():
    """
    Loads a pre-trained translation model and tokenizer from a local directory.
    Returns:
        tokenizer: The tokenizer for the translation model.
        model: The pre-trained translation model.
    """
    model_path = os.path.join(os.path.expanduser("~"), "Downloads", "my_en_vi_translation_model_archive")  
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_path)
        model = MarianMTModel.from_pretrained(model_path)
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model from {model_path}: {e}. Please ensure the model files are present.")
        st.stop()

def translate_text(text: str) -> str:
    """
    Translates English text to Vietnamese using a pre-trained translation model.
    Parameters:
        text (str): The English text to be translated.
    Returns:
        str: The translated text in Vietnamese.
    """
    if not text or not text.strip():
        return "Không có văn bản để dịch."
    
    tokenizer, model = load_translation_model()
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model.generate(**inputs)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

def evaluate_translation(original_text: str, user_translated_text: str):
    """
    Evaluates the quality of a translation by comparing with the machine translation using BLEU score.
    Args:
        original_text (str): The original text in English.
        user_translated_text (str): The translated text in Vietnamese by user.
    Returns:
        tuple: (percentage_correct, machine_translation, comparison)
    """
    if not original_text or not user_translated_text or not original_text.strip() or not user_translated_text.strip():
        return 0.0, "Không có văn bản để so sánh.", "No comparison available."

    tokenizer, model = load_translation_model()
    machine_translation = translate_text(original_text)
    
    user_bleu = sentence_bleu(user_translated_text, [machine_translation]).score
    machine_bleu = 100.0  # Machine translation is reference, so it gets 100%
    percent = user_bleu if user_bleu <= 100 else 100

    if user_bleu > machine_bleu:
        comparison = "User translation is more accurate."
    elif user_bleu < machine_bleu:
        comparison = "Machine translation is more accurate."
    else:
        comparison = "User and machine translations have similar accuracy."

    return percent, machine_translation, comparison

def save_translation_history(user_id, original_text, user_translation, machine_translation, score):
    """
    Placeholder for saving translation history to database.
    Args:
        user_id (int): The user's ID.
        original_text (str): The original English text.
        user_translation (str): The user's translation.
        machine_translation (str): The machine's translation.
        score (float): The BLEU score of the user's translation.
    """
    # Implement database saving logic here (e.g., using SQLite)
    st.write(f"Saving history: User {user_id}, Text: {original_text}, User Trans: {user_translation}, Machine Trans: {machine_translation}, Score: {score}")
    # Example: Replace with actual DB call
    # db.execute("INSERT INTO translation_history (...) VALUES (?, ?, ?, ?, ?)", (user_id, original_text, user_translation, machine_translation, score))
