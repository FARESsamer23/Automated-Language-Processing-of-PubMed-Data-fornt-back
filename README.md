# Automated Language Processing of PubMed Data (Backend & Frontend)

## Overview
This project implements a complete Natural Language Processing (NLP) pipeline for analyzing biomedical text extracted from PubMed abstracts. It was developed as part of the **M1 Data Science & NLP – Computational Linguistics** course.

The system transforms raw medical abstracts into structured linguistic and thematic insights using modern NLP techniques.

---

## Features
- Sentence segmentation from PubMed abstracts
- Morphosyntactic analysis (parsing trees)
- Part-of-Speech (POS) tagging using probabilistic matrices
- Named Entity Recognition (NER)
- Bigram Language Modeling with Laplace smoothing
- Topic Modeling using LDA (Gensim)
- Corpus-wide statistics generation
- Interactive backend for frontend integration

---

## Project Structure

backend/
│
├── api/
│ └── app.py # FastAPI backend
│
├── data/
│ ├── raw/ # Original PubMed data
│ └── processed/
│ ├── sentences.json
│ └── statistics.json
│
├── models/
│ ├── language_model.pkl
│ ├── lda_model.pkl
│ ├── lda_dict.pkl
│ ├── pos_matrices.pkl
│ └── ner_matrices.pkl
│
├── src/
│ ├── preprocessing.py
│ ├── morphosyntax.py
│ ├── pos_tagger.py
│ ├── ner_tagger.py
│ ├── language_model.py
│ ├── topic_model.py
│ ├── statistics.py
│ ├── text_utils.py
│ └── models_classes.py
│
└── requirements.txt

yaml
Copy code

---

## Technologies Used
- Python 3.10+
- FastAPI
- spaCy
- NLTK
- Gensim
- Benepar
- Pickle (model serialization)

---

## Why Pickle (.pkl)?
Pickle is used to serialize trained NLP models (LDA, language model, POS/NER matrices) so they can be:
- Loaded instantly without retraining
- Reused by the backend API
- Consistent across executions

---

## How to Run the Backend

```bash
pip install -r requirements.txt
python backend/api/app.py
