import nltk
from nltk.corpus import wordnet
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from services.translate import translate_text, load_translation_model
# Download required NLTK data
nltk.download('wordnet')

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
        translation = translate_text(definition)
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
