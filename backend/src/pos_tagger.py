import json
import nltk
import pickle
from collections import defaultdict
from pathlib import Path

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def create_pos_matrix(sentences):
    transitions = defaultdict(lambda: defaultdict(int))
    tag_counts = defaultdict(int)

    for sent in sentences:
        tokens = nltk.word_tokenize(sent)
        tags = nltk.pos_tag(tokens)
        prev_tag = "<START>"
        for _, tag in tags:
            transitions[prev_tag][tag] += 1
            tag_counts[prev_tag] += 1
            prev_tag = tag
        transitions[prev_tag]["<END>"] += 1
        tag_counts[prev_tag] += 1

    prob_matrix = {}
    for prev_tag, next_tags in transitions.items():
        total = tag_counts[prev_tag]
        prob_matrix[prev_tag] = {k: v/total for k, v in next_tags.items()}
    return prob_matrix

def run_pos_tagger(input_json_path, output_model_path):
    project_root = Path(__file__).parent.parent
    data_path = project_root / input_json_path
    output_path = project_root / output_model_path

    with open(data_path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)

    matrix = create_pos_matrix(sentences)
    with open(output_path, 'wb') as f:
        pickle.dump(matrix, f)
    print(f"[POSTagger] Matrix saved to {output_path}")

if __name__ == "__main__":
    run_pos_tagger("data/processed/sentences.json", "models/pos_matrices.pkl")
