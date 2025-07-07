from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import streamlit as st
from bert_score import score
import nltk
from utils import nltk_config
from nltk.corpus import wordnet

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

def evaluate_translation(original_text: str, user_translated_text: str):
    """
    Evaluates the quality of a translation using BERTScore.
    Args:
        original_text (str): The original text in English.
        user_translated_text (str): The translated text in Vietnamese by user.
    Returns:
        tuple: (percentage_correct, machine_translation)
    """
    if not original_text or not user_translated_text or not original_text.strip() or not user_translated_text.strip():
        return 0.0, "Không có văn bản để so sánh.", "No comparison available."

    machine_translation = translate_text(original_text)

    P, R, F1 = score([user_translated_text], [machine_translation], lang="vi", model_type="distilbert-base-multilingual-cased")
    percent = F1.mean().item() * 100

    return percent, machine_translation

# Hàm lấy thông tin từ WordNet (nếu là từ đơn)
@st.cache_data(show_spinner=False)
def get_wordnet_info(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return None
    synset = synsets[0]  # Lấy synset đầu tiên
    return {
        "definition": synset.definition(),
        "examples": synsets[0].examples(),
        "synonyms": [lemma.name() for lemma in synset.lemmas()],
        "pos": synset.pos()
    }