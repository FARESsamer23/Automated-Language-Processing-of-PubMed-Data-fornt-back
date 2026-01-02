import os
import sys
import pickle
import json
from pathlib import Path
from typing import List
import nltk
import spacy
import benepar
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- 1. Path & Import Setup ---
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "src"))

# Fix for the Pickle Attribute Error
try:
    from src.models_classes import LanguageModel
except ImportError:
    from models_classes import LanguageModel

# --- 2. FastAPI Setup ---
app = FastAPI(title="NLP Project Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Resource Loading ---
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

try:
    nlp = spacy.load("en_core_web_sm")
    if "benepar" not in nlp.pipe_names:
        nlp.add_pipe("benepar", config={"model": "benepar_en3"})
    print("✓ Spacy and Benepar loaded successfully")
except Exception as e:
    print(f"⚠ Benepar fallback: {e}")
    nlp = spacy.load("en_core_web_sm")

# --- 4. Load Pickle Models ---
MODELS_DIR = BASE_DIR / "models"

def load_pickle(filename):
    try:
        with open(MODELS_DIR / filename, "rb") as f:
            print(f"✓ Loaded {filename}")
            return pickle.load(f)
    except Exception as e:
        print(f"⚠ Warning: Could not load {filename}: {e}")
        return None

# Updated to match your screenshot filenames
pos_tagger = load_pickle("pos_matrices.pkl")
ner_tagger = load_pickle("ner_matrices.pkl")
language_model = load_pickle("language_model.pkl") 
lda_model = load_pickle("lda_model.pkl")
lda_dict = load_pickle("lda_dict.pkl")

class TextInput(BaseModel):
    text: str

# --- 5. Endpoints (All 100% Restored) ---

@app.get("/")
def health_check():
    return {"status": "online", "models": {"pos": pos_tagger is not None, "language": language_model is not None}}

@app.get("/statistics")
def get_statistics():
    stats_path = BASE_DIR / "data/processed/statistics.json"
    if not stats_path.exists():
        raise HTTPException(status_code=404, detail="Run src/statistics.py first")
    with open(stats_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/analyze/language/statistics")
def language_statistics():
    if not language_model:
        return {"vocabulary_size": 0, "message": "Model not loaded."}
    return language_model.get_statistics()

@app.post("/analyze/language/bigram-probability")
def bigram_probability(data: TextInput):
    if not language_model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    tokens = data.text.lower().split()
    if len(tokens) < 2:
        raise HTTPException(status_code=400, detail="2 words required")
    probs = []
    for i in range(len(tokens) - 1):
        prob = language_model.get_probability([tokens[i], tokens[i + 1]])
        probs.append({"bigram": f"{tokens[i]} {tokens[i + 1]}", "probability": prob})
    return {"results": probs}

@app.post("/analyze/syntax")
def analyze_syntax(input_data: TextInput):
    doc = nlp(input_data.text)
    tree_string = ""
    for sent in doc.sents:
        if hasattr(sent._, "parse_string"):
            tree_string = str(sent._.parse_string)
            break
    return {"original": input_data.text, "constituency_tree": tree_string}

@app.post("/analyze/ner")
def analyze_ner(input_data: TextInput):
    doc = nlp(input_data.text)
    return {"entities": [{"text": ent.text, "label": ent.label_} for ent in doc.ents]}

@app.post("/analyze/pos")
def pos_analysis(data: TextInput):
    if pos_tagger and hasattr(pos_tagger, 'tag_sentence'):
        tagged = pos_tagger.tag_sentence(data.text)
        return {"tokens": [{"word": w, "tag": t} for w, t in tagged]}
    tokens = nltk.word_tokenize(data.text)
    tagged = nltk.pos_tag(tokens)
    return {"tokens": [{"word": w, "tag": t} for w, t in tagged]}

@app.post("/analyze/topics")
def analyze_topics(input_data: TextInput):
    if not lda_model or not lda_dict:
        raise HTTPException(status_code=503, detail="LDA not loaded")
    tokens = input_data.text.lower().split()
    bow = lda_dict.doc2bow(tokens)
    dist = lda_model.get_document_topics(bow)
    topics = [{"topic_id": tid, "probability": float(p), "keywords": [w for w, _ in lda_model.show_topic(tid, 5)]} for tid, p in dist]
    return {"topics": sorted(topics, key=lambda x: x['probability'], reverse=True)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)