# backend/src/text_utils.py

import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOP_WORDS = set(stopwords.words("english"))

def preprocess_text(text: str):
    tokens = word_tokenize(text.lower())
    tokens = [
        t for t in tokens
        if t.isalnum()
        and t not in STOP_WORDS
    ]
    return tokens
