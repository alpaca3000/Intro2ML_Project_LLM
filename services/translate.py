from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import streamlit as st
from bert_score import score
import os

@st.cache_resource(show_spinner="Đang tải mô hình dịch thuật...")
def load_translation_model():
    """
    Loads a pre-trained translation model and tokenizer from a specified directory.
    Returns:
        tokenizer: The tokenizer for the translation model.
        model: The pre-trained translation model.
    """
    model_path = "alpaca3000/en-vi-translation-model"  
    # model_path = "models/my_en_vi_translation_model_archive"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        model.eval()  # Set the model to evaluation mode
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model from {model_path}: {e}. Please ensure the model is accessible (e.g., online or downloaded).")
        st.stop()

@st.cache_data
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
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=64).to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=64, num_beams=3, early_stopping=True)  # Giảm beams
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

@st.cache_data
def evaluate_translation(original_text: str, user_translated_text: str):
     """
    Evaluates the quality of a translation using BERTScore.
    Args:
        original_text (str): The original text in English.
        user_translated_text (str): The translated text in Vietnamese by user.
    Returns:
        tuple: (percentage_correct, machine_translation, comparison)
    """
    if not original_text or not user_translated_text or not original_text.strip() or not user_translated_text.strip():
        return 0.0, "Không có văn bản để so sánh.", "No comparison available."

    machine_translation = translate_text(original_text)
    
    P, R, F1 = score([user_translated_text], [machine_translation], lang="vi", model_type="distilbert-base-multilingual-cased")
    percent = F1.mean().item() * 100

    if percent >= 80:
        comparison = "User translation is highly accurate."
    elif percent >= 50:
        comparison = "User translation is semantically acceptable."
    else:
        comparison = "Machine translation is more accurate."

    return percent, machine_translation, comparison
    
def save_translation_history(user_id, original_text, user_translation, machine_translation, score):
    """
    Placeholder for saving translation history to database.
    Args:
        user_id (int): The user's ID.
        original_text (str): The original English text.
        user_translation (str): The user's translation.
        machine_translation (str): The machine's translation.
        score (float): The BERTScore of the user's translation.
    """
    st.write(f"Saving history: User {user_id}, Text: {original_text}, User Trans: {user_translation}, Machine Trans: {machine_translation}, Score: {score}")
    # Replace with actual DB call
