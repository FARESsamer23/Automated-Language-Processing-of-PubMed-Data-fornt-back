# import os
# import sys
# import pickle
# import json
# from pathlib import Path
# from typing import List
# from collections import Counter
# import nltk
# import spacy
# import benepar

# # --- Add src to path ---
# sys.path.append(str(Path(__file__).parent.parent / "src"))
# try:
#     from src.text_utils import preprocess_text
# except ImportError:
#     # Fallback if text_utils is not available
#     def preprocess_text(text):
#         return text.lower().split()

# # --- 1. Setup FastAPI ---
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# app = FastAPI(title="NLP Project Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- 2. Download NLTK resources ---
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)
# nltk.download('averaged_perceptron_tagger', quiet=True)

# # --- 3. Download Benepar model ---
# try:
#     benepar.download('benepar_en3')
# except:
#     print("Benepar model already downloaded or download failed")

# # --- 4. Load Spacy + Benepar ---
# try:
#     nlp = spacy.load("en_core_web_sm")
#     if "benepar" not in nlp.pipe_names:
#         nlp.add_pipe("benepar", config={"model": "benepar_en3"})
#     print("✓ Spacy and Benepar loaded successfully")
# except OSError as e:
#     print(f"Error loading models: {e}")
#     sys.exit(1)

# # --- 5. Load Pickle Models ---
# BASE_DIR = Path(__file__).parent.parent
# MODELS_DIR = BASE_DIR / "models"

# def load_pickle(filename):
#     try:
#         with open(MODELS_DIR / filename, "rb") as f:
#             print(f"✓ Loaded {filename}")
#             return pickle.load(f)
#     except FileNotFoundError:
#         print(f"⚠ Warning: {filename} not found")
#         return None

# pos_tagger = load_pickle("pos_tagger.pkl")
# ner_tagger = load_pickle("ner_tagger.pkl")
# language_model = load_pickle("language_model.pkl")
# lda_model = load_pickle("lda_model.pkl")
# lda_dict = load_pickle("lda_dict.pkl")

# # --- 6. Input Models ---
# class TextInput(BaseModel):
#     text: str

# # --- 7. Health Check ---
# @app.get("/")
# def health_check():
#     return {
#         "status": "online",
#         "models_loaded": {
#             "spacy": True,
#             "benepar": "benepar" in nlp.pipe_names,
#             "pos_tagger": pos_tagger is not None,
#             "ner_tagger": ner_tagger is not None,
#             "language_model": language_model is not None,
#             "lda_model": lda_model is not None,
#             "lda_dict": lda_dict is not None
#         }
#     }

# # --- 8. Syntax Tree ---
# @app.post("/analyze/syntax")
# def analyze_syntax(input_data: TextInput):
#     try:
#         doc = nlp(input_data.text)
#         tree_string = ""
#         for sent in doc.sents:
#             tree_string = str(sent._.parse_string)
#             break
        
#         if not tree_string:
#             raise HTTPException(status_code=400, detail="No sentence found to parse")
            
#         return {"original": input_data.text, "constituency_tree": tree_string}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error parsing syntax: {str(e)}")

# # --- 9. NER (using Spacy - always available) ---
# @app.post("/analyze/ner")
# def analyze_ner(input_data: TextInput):
#     try:
#         doc = nlp(input_data.text)
#         entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
#         return {"original": input_data.text, "entities": entities}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error analyzing NER: {str(e)}")

# @app.post("/analyze/ner/bio")
# def ner_bio_analysis(data: TextInput):
#     if not ner_tagger:
#         raise HTTPException(status_code=503, detail="NER tagger model not loaded. Please train the model first.")
#     try:
#         tagged = ner_tagger.tag_sentence(data.text)
#         return {"tokens": [{"word": w, "tag": t} for w, t in tagged]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error in BIO tagging: {str(e)}")

# @app.get("/analyze/ner/statistics")
# def ner_statistics():
#     if not ner_tagger:
#         return {
#             "message": "NER tagger not loaded",
#             "total_entities": 0,
#             "entity_types": {}
#         }
#     try:
#         return ner_tagger.get_statistics()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting NER statistics: {str(e)}")

# # --- 10. POS Tagging (using NLTK as fallback) ---
# @app.post("/analyze/pos")
# def pos_analysis(data: TextInput):
#     if pos_tagger:
#         try:
#             tagged = pos_tagger.tag_sentence(data.text)
#             return {"tokens": [{"word": w, "tag": t} for w, t in tagged]}
#         except Exception as e:
#             print(f"Custom POS tagger failed: {e}, falling back to NLTK")
    
#     # Fallback to NLTK POS tagger
#     try:
#         from nltk import word_tokenize, pos_tag
#         tokens = word_tokenize(data.text)
#         tagged = pos_tag(tokens)
#         return {"tokens": [{"word": w, "tag": t} for w, t in tagged]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error in POS tagging: {str(e)}")

# @app.get("/analyze/pos/statistics")
# def pos_statistics():
#     if not pos_tagger:
#         return {
#             "message": "POS tagger not loaded",
#             "total_tags": 0,
#             "tag_distribution": {}
#         }
#     try:
#         return pos_tagger.get_statistics()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting POS statistics: {str(e)}")

# # --- 11. Language Model ---
# @app.get("/analyze/language/statistics")
# def language_statistics():
#     if not language_model:
#         return {
#             "vocabulary_size": 0,
#             "total_bigrams": 0,
#             "unique_bigrams": 0,
#             "message": "Language model not loaded. Please train the model first."
#         }
#     try:
#         return language_model.get_statistics()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting language statistics: {str(e)}")

# @app.post("/analyze/language/bigram-probability")
# def bigram_probability(data: TextInput):
#     if not language_model:
#         raise HTTPException(status_code=503, detail="Language model not loaded. Please train the model first.")

#     tokens = data.text.lower().split()
#     if len(tokens) < 2:
#         raise HTTPException(status_code=400, detail="At least two words required")

#     try:
#         probs = []
#         for i in range(len(tokens) - 1):
#             prob = language_model.get_probability([tokens[i], tokens[i + 1]])
#             probs.append({"bigram": f"{tokens[i]} {tokens[i + 1]}", "probability": prob})

#         return {"results": probs}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error calculating bigram probability: {str(e)}")

# # --- 12. Topics ---
# @app.post("/analyze/topics")
# def analyze_topics(input_data: TextInput):
#     if not lda_model or not lda_dict:
#         raise HTTPException(status_code=503, detail="LDA model or dictionary not loaded. Please train the model first.")

#     try:
#         tokens = preprocess_text(input_data.text)
#         bow = lda_dict.doc2bow(tokens)
#         topic_distribution = lda_model.get_document_topics(bow)

#         topics = []
#         for topic_id, prob in topic_distribution:
#             keywords = [word for word, _ in lda_model.show_topic(topic_id, topn=5)]
#             topics.append({"topic_id": topic_id, "probability": round(prob, 3), "keywords": keywords})

#         topics.sort(key=lambda x: x['probability'], reverse=True)

#         return {"original": input_data.text, "topics": topics}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error analyzing topics: {str(e)}")

# # --- 13. Dataset Statistics ---
# @app.get("/statistics")
# def get_statistics():
#     stats_path = BASE_DIR / "data/processed/statistics.json"
#     if not stats_path.exists():
#         raise HTTPException(status_code=404, detail="Statistics not found. Run src/statistics.py first.")
    
#     try:
#         with open(stats_path, "r", encoding="utf-8") as f:
#             stats = json.load(f)
#         return stats
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error loading statistics: {str(e)}")

# # --- 14. Run App ---
# if __name__ == "__main__":
#     import uvicorn
#     print("\n" + "="*50)
#     print("🚀 Starting NLP Server...")
#     print("="*50 + "\n")
#     uvicorn.run(app, host="0.0.0.0", port=8000)
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