from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import streamlit as st

@st.cache_resource(show_spinner="Đang tải mô hình dịch thuật...")
def load_translation_model():
    """
    Loads a pre-trained translation model and tokenizer.
    returns:
        tokenizer: The tokenizer for the translation model.
        model: The pre-trained translation model.
    """
    model_path = "alpaca3000/en-vi-translation-model"
    #model_path = "models/my_en_vi_translation_model_archive"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    model.eval()  # Set the model to evaluation mode
    return tokenizer, model

def translate_text(text: str) -> str:
    """
    Translates English text to Vietnamese using a pre-trained translation model.
    parameters:
        text (str): The English text to be translated.
    returns:
        str: The translated text in Vietnamese.
    """
    tokenizer, model = load_translation_model()

    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=128, num_beams=5, early_stopping=True)
    
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

def evaluate_translation(original_text, user_translated_text):
    """
    Evaluates the quality of a translation by comparing the original text with the translated text.
    
    Args:
        original_text (str): The original text in English.
        translated_text (str): The translated text in Vietnamese.
        
    Returns:
        str: A message indicating whether the translation is correct or not.
    """
    # Placeholder for evaluation logic
    # In a real application, this could involve checking for accuracy, fluency, etc.
    model_translated_text = translate_text(original_text)
    
    correct_count = sum(1 for a, b in zip(model_translated_text, user_translated_text) if a == b)
    total_count = max(len(model_translated_text), len(user_translated_text))
    if total_count == 0:
        return "Không có văn bản để so sánh."
    percentage_correct = (correct_count / total_count) * 100

    return percentage_correct, model_translated_text # Simulate a percentage of correctness   