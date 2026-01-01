import json
from collections import Counter
from pathlib import Path
import nltk

nltk.download('punkt', quiet=True)

def compute_statistics(input_json_path, output_json_path):
    project_root = Path(__file__).parent.parent
    data_path = project_root / input_json_path
    output_path = project_root / output_json_path

    # Load sentences
    with open(data_path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)

    total_sentences = len(sentences)
    all_words = []

    # Tokenize words for all sentences
    for sent in sentences:
        words = nltk.word_tokenize(sent.lower())
        all_words.extend(words)

    total_words = len(all_words)
    word_counts = Counter(all_words)
    most_common_words = word_counts.most_common(20)  # top 20 words

    # Bigram frequencies
    bigrams = list(nltk.bigrams(all_words))
    bigram_counts = Counter(bigrams)
    most_common_bigrams = [(" ".join(b), c) for b, c in bigram_counts.most_common(20)]

    # Save statistics
    stats = {
        "total_sentences": total_sentences,
        "total_words": total_words,
        "most_common_words": most_common_words,
        "most_common_bigrams": most_common_bigrams
    }

    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4)

    print(f"[Statistics] Saved statistics to {output_path}")

if __name__ == "__main__":
    compute_statistics(
        input_json_path="data/processed/sentences.json",
        output_json_path="data/processed/statistics.json"
    )
