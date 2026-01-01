# src/models_classes.py
from collections import defaultdict

class LanguageModel:
    def __init__(self, n=2):
        self.n = n
        self.ngrams = defaultdict(int)
        self.contexts = defaultdict(int)
        self.vocab = set()
        self.vocab_size = 0

    def train(self, sentences):
        for sent in sentences:
            tokens = ['<s>'] + sent.lower().split() + ['</s>']
            self.vocab.update(tokens)
            for i in range(len(tokens)-self.n+1):
                ngram = tuple(tokens[i:i+self.n])
                context = tuple(tokens[i:i+self.n-1])
                self.ngrams[ngram] += 1
                self.contexts[context] += 1
        self.vocab_size = len(self.vocab)

    def get_statistics(self):
        return {
            "vocabulary_size": self.vocab_size,
            "total_bigrams": sum(self.ngrams.values()),
            "unique_bigrams": len(self.ngrams)
        }

    def get_probability(self, ngram):
        count_ngram = self.ngrams.get(tuple(ngram), 0)
        context = tuple(ngram[:-1])
        count_context = self.contexts.get(context, 0)
        return (count_ngram + 1) / (count_context + self.vocab_size)