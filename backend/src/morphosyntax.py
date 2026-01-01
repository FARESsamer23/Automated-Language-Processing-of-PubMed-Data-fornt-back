import spacy
import benepar
from nltk import Tree
import json
from pathlib import Path

# Download Benepar model (run once)
benepar.download('benepar_en3')

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Add Benepar component for parsing
if "benepar" not in nlp.pipe_names:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

def analyze_syntax(input_json_path):
    project_root = Path(__file__).parent.parent
    data_path = project_root / input_json_path
    
    # Load sentences from JSON
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sentences = data[:5]  # just the first 5 for testing
    for sent in sentences:
        doc = nlp(sent)
        for const_sent in doc.sents:
            tree_str = const_sent._.parse_string
            tree = Tree.fromstring(tree_str)

            # Print the tree in text form (top-down)
            print(tree.pformat(margin=100))

            # Optional: open a graphical window to show the tree
            # tree.draw()  

            print("-" * 50)

if __name__ == "__main__":
    analyze_syntax("data/processed/sentences.json")
