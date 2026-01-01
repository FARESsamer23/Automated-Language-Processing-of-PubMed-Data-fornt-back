# import json
# from collections import defaultdict
# from pathlib import Path

# class LanguageModel:
#     def __init__(self, n=2):
#         self.n = n
#         self.ngrams = defaultdict(int)
#         self.contexts = defaultdict(int)
#         self.vocab = set()
#         self.vocab_size = 0

#     def train(self, sentences):
#         for sent in sentences:
#             tokens = ['<s>'] + sent.lower().split() + ['</s>']
#             self.vocab.update(tokens)
#             for i in range(len(tokens)-self.n+1):
#                 ngram = tuple(tokens[i:i+self.n])
#                 context = tuple(tokens[i:i+self.n-1])
#                 self.ngrams[ngram] += 1
#                 self.contexts[context] += 1
#         self.vocab_size = len(self.vocab)
#         print(f"[LanguageModel] Trained {self.n}-gram. Vocab size: {self.vocab_size}")

#     def get_probability(self, ngram):
#         count_ngram = self.ngrams.get(tuple(ngram), 0)
#         context = tuple(ngram[:-1])
#         count_context = self.contexts.get(context, 0)
#         return (count_ngram + 1) / (count_context + self.vocab_size)

# def run_modeling(input_json_path):
#     project_root = Path(__file__).parent.parent
#     data_path = project_root / input_json_path
    
#     with open(data_path, 'r', encoding='utf-8') as f:
#         sentences = json.load(f)
    
#     lm = LanguageModel(n=2)
#     lm.train(sentences)
#     print("[LanguageModel] Training complete.")

# if __name__ == "__main__":
#     run_modeling("data/processed/sentences.json")
import json
import pickle
from pathlib import Path
from models_classes import LanguageModel # Import from shared file

def run_modeling(input_json_path):
    project_root = Path(__file__).parent.parent
    data_path = project_root / input_json_path
    models_dir = project_root / "models"
    models_dir.mkdir(exist_ok=True)
    
    with open(data_path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)
    
    lm = LanguageModel(n=2)
    lm.train(sentences)
    
    with open(models_dir / "language_model.pkl", "wb") as f:
        pickle.dump(lm, f)
    print("✓ Model saved successfully.")

if __name__ == "__main__":
    run_modeling("data/processed/sentences.json")
    