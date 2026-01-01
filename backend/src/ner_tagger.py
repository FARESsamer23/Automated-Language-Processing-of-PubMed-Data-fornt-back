import json
import spacy
import pickle
from collections import defaultdict
from pathlib import Path

nlp = spacy.load("en_core_web_sm")

def create_ner_matrix(sentences):
    transitions = defaultdict(lambda: defaultdict(int))
    tag_counts = defaultdict(int)

    for sent in sentences:
        doc = nlp(sent)
        tags = ["O"] * len(doc)
        for ent in doc.ents:
            for i in range(ent.start, ent.end):
                if i == ent.start:
                    tags[i] = f"B-{ent.label_}"
                else:
                    tags[i] = f"I-{ent.label_}"
        prev_tag = "<START>"
        for tag in tags:
            transitions[prev_tag][tag] += 1
            tag_counts[prev_tag] += 1
            prev_tag = tag
        transitions[prev_tag]["<END>"] += 1
        tag_counts[prev_tag] += 1

    prob_matrix = {prev: {k: v/sum(next_tags.values()) for k, v in next_tags.items()} for prev, next_tags in transitions.items()}
    return prob_matrix

def run_ner(input_json_path, output_model_path):
    project_root = Path(__file__).parent.parent
    data_path = project_root / input_json_path
    output_path = project_root / output_model_path

    with open(data_path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)

    matrix = create_ner_matrix(sentences)
    with open(output_path, 'wb') as f:
        pickle.dump(matrix, f)
    print(f"[NERTagger] Matrix saved to {output_path}")

if __name__ == "__main__":
    run_ner("data/processed/sentences.json", "models/ner_matrices.pkl")
