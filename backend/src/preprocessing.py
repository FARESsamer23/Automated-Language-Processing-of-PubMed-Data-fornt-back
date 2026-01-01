import os
import json
from lxml import etree
import nltk

# Download tokenizer
nltk.download('punkt', quiet=True)

def extract_abstracts(xml_file_path, output_json_path, max_abstracts=40):
    sentences = []
    abstracts_count = 0

    print(f"[Preprocessing] Extracting from {xml_file_path}...")

    context = etree.iterparse(xml_file_path, events=('end',), tag='PubmedArticle')
    for _, elem in context:
        if abstracts_count >= max_abstracts:
            break

        abstract_texts = elem.xpath('.//Abstract/AbstractText/text()')
        if abstract_texts:
            full_abstract = " ".join(abstract_texts)
            abstracts_count += 1
            sentences.extend(nltk.sent_tokenize(full_abstract))
        elem.clear()

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(sentences, f, indent=4)

    print(f"[Preprocessing] Saved {len(sentences)} sentences from {abstracts_count} abstracts to {output_json_path}")
    return sentences

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(project_root, "data", "raw", "test.xml")
    processed_path = os.path.join(project_root, "data", "processed", "sentences.json")

    extract_abstracts(raw_path, processed_path, max_abstracts=80)
