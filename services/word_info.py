import nltk
from nltk.corpus import wordnet
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# Download required NLTK data
nltk.download('wordnet')
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
    return tokenizer, model
# Additional functions for get_word_info function
def transfer_part_of_speech(pos):
    if pos == "n":
        return "Danh từ"
    elif pos == "v":
        return "Động từ"
    elif pos == "a":
        return "Tính từ"
    elif pos == "r":
        return "Trạng từ"
    elif pos == "s":
        return "Đại từ"
def translate_word(word):
    tokenizer, model = load_translation_model()
    input = tokenizer(word, return_tensors="pt", padding=True, truncation=True, max_length=128)

    with torch.no_grad():
        outputs = model.generate(**input, max_length=128, num_beams=5, early_stopping=True)
            
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation
def upper_first_letter(word):
    return word[0].upper() + word[1:]
# Get information of a word
def get_word_info(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return []
    
    result = []
    for synset in synsets:
        # Get definitions
        info = {}
        definition = synset.definition()
        translation = translate_word(definition)
        translation = upper_first_letter(translation)
        info['definition'] = translation
        
        # Get examples
        info['examples'] = []
        if synset.examples():
            for example in synset.examples():
                example = upper_first_letter(example)
                info['examples'].append(example)
        
        # Get synonyms
        synonyms = [lemma.name() for lemma in synset.lemmas() if lemma.name() != word]
        if synonyms:
            info['synonyms'] = synonyms
        
        # Get part of speech
        info['part_of_speech'] = transfer_part_of_speech(synset.pos())
        result.append(info)
    
    return result

# def _main():
#     word = "friendly"
#     word_info = get_word_info(word)
#     print(f"Từ: {word}")
#     for info in word_info:
#         print("--------------------------------")
#         print(f"Định nghĩa: {info['definition']}")
#         print(f"Ví dụ:")
#         for example in info['examples']:
#             print(f"- {example}")
#         if 'synonyms' in info:
#             print(f"Từ đồng nghĩa: {', '.join(info['synonyms'])}")
#         print(f"Loại từ: {info['part_of_speech']}")

# if __name__ == "__main__":
#     _main()
