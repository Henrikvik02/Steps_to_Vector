from pathlib import Path
import spacy
from spacy.tokens import DocBin
import json
import random

def convert_spacyjson_docs(file_path, train_file_path, test_file_path, lang_model="nb_core_news_lg", split_ratio=0.8):
    nlp = spacy.load(lang_model)

    # Ensure the output directories exist
    Path(train_file_path).parent.mkdir(parents=True, exist_ok=True)
    Path(test_file_path).parent.mkdir(parents=True, exist_ok=True)

    training_data = []
    # Load JSONL data
    with open(file_path, 'r', encoding='utf-8') as json_file:
        training_data = [json.loads(line) for line in json_file]

    # Shuffle and split the data
    random.shuffle(training_data)
    split_at = int(len(training_data) * split_ratio)
    train_data = training_data[:split_at]
    test_data = training_data[split_at:]

    # Function to process and add documents to DocBin
    def process_data(data, doc_bin):
        for text, annotations in data:
            doc = nlp.make_doc(text)
            ents = []
            for start, end, label in annotations["entities"]:
                span = doc.char_span(start, end, label=label)
                if span is not None:  # Ensure the span is valid
                    ents.append(span)
            doc.ents = ents
            doc_bin.add(doc)

    # Create and save training DocBin
    train_db = DocBin()
    process_data(train_data, train_db)
    train_db.to_disk(train_file_path)

    # Create and save test DocBin
    test_db = DocBin()
    process_data(test_data, test_db)
    test_db.to_disk(test_file_path)

# Corrected example usage
file_path = './data/annotated/processed/spacyall4.jsonl'
train_file_path = './data/annotated/spacy/training.spacy'
test_file_path = './data/annotated/spacy/test.spacy'  # Corrected the path
convert_spacyjson_docs(file_path, train_file_path, test_file_path)
