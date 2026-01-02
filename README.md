# Automated Language Processing of PubMed Data

## Overview

This project is a **full-stack Natural Language Processing (NLP) system** designed to process, analyze, and visualize textual data extracted from **PubMed abstracts**. It combines:

* A **React frontend** for interactive analysis and visualization
* A **FastAPI backend** exposing NLP services via REST APIs
* Multiple **NLP pipelines** (NER, POS tagging, Syntax Parsing, Topic Modeling, Language Modeling, and Statistics)
* **Pre-trained and custom-trained models** serialized using Pickle (`.pkl`)

The system is modular, reproducible, and suitable for academic projects in NLP, data science, and applied AI.

---

## System Architecture

```
PubMed XML
   ↓
Preprocessing (XML → Sentences JSON)
   ↓
Model Training (POS, NER, LDA, N-grams)
   ↓
Pickle Models (.pkl)
   ↓
FastAPI Backend (REST APIs)
   ↓
React Frontend (Visualization & Interaction)
```

---

## Frontend (React)

### Common Design Principles

All frontend analyzers share:

* Text input OR `.txt` file upload
* Maximum input size: **500 words** (client-side validation)
* Async API calls with loading state
* TailwindCSS-based modern UI

The frontend communicates exclusively with the backend via `services/api.js`.

---

### 1. Named Entity Recognition (NERAnalyzer)

**Purpose**: Extract structured entities from raw text.

**Entities Supported**:

* PERSON
* ORG (Organization)
* GPE (Geo-political entity)
* LOC
* DATE, TIME, MONEY

**Workflow**:

1. User inputs text or uploads a file
2. Frontend calls `POST /analyze/ner`
3. Backend uses spaCy NER
4. Results are color-coded by entity type

**Key Features**:

* Dynamic entity styling
* Token-level visualization
* Real-time feedback

---

### 2. Part-of-Speech Tagging (POSAnalyzer)

**Purpose**: Assign grammatical categories to tokens.

**POS Tags**:

* NN*: Nouns
* VB*: Verbs
* JJ*: Adjectives
* RB*: Adverbs
* PR*: Pronouns

**Workflow**:

1. Text input / file upload
2. API call to `POST /analyze/pos`
3. Backend uses:

   * Custom Markov model (if available)
   * Fallback: NLTK POS tagger

**Visualization**:

* Token cards
* Color-coded POS tags

---

### 3. Syntax Analyzer (Constituency Parsing)

**Purpose**: Visualize grammatical structure of sentences.

**Backend Model**:

* spaCy + Benepar (Berkeley Neural Parser)

**Two View Modes**:

* **Tree View**: Recursive React tree visualization
* **Text View**: Penn Treebank-style bracket notation

**Workflow**:

1. `POST /analyze/syntax`
2. Backend returns constituency tree string
3. Frontend parses string into a tree structure

---

### 4. Topic Modeling (TopicAnalyzer)

**Purpose**: Discover latent themes in text.

**Algorithm**:

* Latent Dirichlet Allocation (LDA)

**Design Choices**:

* Exactly **3 topics**
* Only top keywords displayed

**Workflow**:

1. Pretrained LDA model is loaded
2. Text → Bag-of-Words
3. Topic probabilities returned

---

### 5. Statistics Dashboard

**Purpose**: Dataset-level analytics.

**Displayed Metrics**:

* Total sentences
* Total words
* Vocabulary size
* Average sentence length
* Top 20 words
* Top 10 bigrams

**Backend Sources**:

* `statistics.json`
* Language model metadata

---

## Backend (FastAPI)

### Core Responsibilities

* Model loading
* Text processing
* REST API exposure
* Serialization/deserialization of models

---

### 1. Data Preprocessing (PubMed XML)

**File**: `extract_abstracts.py`

**Functionality**:

* Parses PubMed XML
* Extracts abstract text
* Sentence tokenization (NLTK)
* Saves output as JSON

**Output**:

```
data/processed/sentences.json
```

---

### 2. Statistics Computation

**File**: `statistics.py`

**Computed Metrics**:

* Sentence count
* Word count
* Word frequencies
* Bigram frequencies

**Saved as**:

```
data/processed/statistics.json
```

---

### 3. Language Model (N-gram)

**Class**: `LanguageModel` (models_classes.py)

**Model Type**:

* Bigram language model (n=2)
* Add-one (Laplace) smoothing

**Stored Data**:

* Vocabulary
* Bigram counts
* Context counts

**Why Pickle?**

* Python-native serialization
* Preserves class methods
* Fast loading at runtime

**Saved as**:

```
models/language_model.pkl
```

---

### 4. POS Tagger Model

**Approach**:

* Markov transition matrix of POS tags

**Training**:

* NLTK tokenization + tagging
* Transition probabilities stored

**Saved as**:

```
models/pos_matrices.pkl
```

---

### 5. NER Transition Model

**Approach**:

* BIO tagging scheme (B-ENT / I-ENT)
* spaCy-generated labels

**Purpose**:

* Educational modeling of NER transitions

**Saved as**:

```
models/ner_matrices.pkl
```

---

### 6. Topic Modeling (LDA)

**Libraries**:

* spaCy (preprocessing)
* Gensim (LDA)

**Preprocessing Steps**:

* Lemmatization
* Stopword removal
* POS filtering (NOUN, PROPN, ADJ)
* Dictionary pruning

**Artifacts**:

```
models/lda_model.pkl
models/lda_dict.pkl
```

---

### 7. FastAPI Endpoints

| Endpoint                               | Method | Description              |
| -------------------------------------- | ------ | ------------------------ |
| `/`                                    | GET    | Health check             |
| `/statistics`                          | GET    | Dataset statistics       |
| `/analyze/language/statistics`         | GET    | Language model stats     |
| `/analyze/language/bigram-probability` | POST   | Bigram probabilities     |
| `/analyze/syntax`                      | POST   | Constituency parsing     |
| `/analyze/ner`                         | POST   | Named Entity Recognition |
| `/analyze/pos`                         | POST   | POS tagging              |
| `/analyze/topics`                      | POST   | Topic modeling           |

---

## Why `.pkl` Files Are Used

Pickle files are used to:

* Persist trained models
* Avoid retraining on every startup
* Ensure consistent results
* Speed up backend initialization

Each `.pkl` corresponds to a **trained intelligence artifact**, not raw data.

---

## Project Strengths

* End-to-end NLP pipeline
* Clear separation of concerns
* Academic + production-ready design
* Modular and extensible
* Suitable for research, demos, and teaching

---

## Notes

* `test.xml` should NOT be pushed to GitHub (large raw data)
* Add it to `.gitignore`

---

## Author

**Samer Fares**
Master 1 Data Science – NLP Track
Full-Stack & AI-Oriented Developer

---


