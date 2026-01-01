import json
import pickle
import spacy
from pathlib import Path
from gensim import corpora, models

# Load spaCy for professional-grade preprocessing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def preprocess_docs(sentences):
    """
    Cleans text by:
    1. Removing stop words and punctuation.
    2. Keeping only Nouns, Proper Nouns, and Adjectives.
    3. Lemmatizing words (e.g., 'surgery' and 'surgeries' become the same token).
    """
    processed_docs = []
    for doc in sentences:
        spacy_doc = nlp(doc.lower())
        # Filter: keep only meaningful parts of speech and exclude short words
        tokens = [
            token.lemma_ for token in spacy_doc 
            if token.pos_ in ["NOUN", "PROPN", "ADJ"] 
            and not token.is_stop 
            and token.is_alpha
            and len(token.text) > 2
        ]
        processed_docs.append(tokens)
    return processed_docs

def run_topic_modeling(input_json_path, output_model_path, output_dict_path):
    project_root = Path(__file__).parent.parent
    data_path = project_root / input_json_path
    model_path = project_root / output_model_path
    dict_path = project_root / output_dict_path

    # Ensure output directory exists
    model_path.parent.mkdir(exist_ok=True)

    if not data_path.exists():
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)

    print(f"[TopicModel] Preprocessing {len(sentences)} sentences...")
    processed_docs = preprocess_docs(sentences)

    # Create Dictionary
    dictionary = corpora.Dictionary(processed_docs)
    
    # NEW: Filter extremes to remove noise
    # Filter words that appear in fewer than 2 docs or more than 70% of docs
    dictionary.filter_extremes(no_below=2, no_above=0.7)
    
    # Create Corpus
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    print("[TopicModel] Training LDA model...")
    # Increase passes and iterations for better accuracy
    lda_model = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=3, 
        random_state=100,
        update_every=1,
        chunksize=100,
        passes=20,          # Increased for better convergence
        alpha='auto',
        per_word_topics=True
    )

    # Save outputs
    with open(model_path, "wb") as f:
        pickle.dump(lda_model, f)
    with open(dict_path, "wb") as f:
        pickle.dump(dictionary, f)

    print(f"[TopicModel] Success! Model saved to {output_model_path}")
    
    # Print the topics for verification
    for idx, topic in lda_model.print_topics(-1):
        print(f"Topic {idx}: {topic}")

if __name__ == "__main__":
    run_topic_modeling(
        "data/processed/sentences.json", 
        "models/lda_model.pkl", 
        "models/lda_dict.pkl"
    )