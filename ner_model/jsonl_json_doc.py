import json
import spacy
from spacy.tokens import DocBin


def convert_jsonl_to_spacy_json(input_file_path, output_file_path):
    training_data = []
    with open(input_file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            text = data['text']
            entities = data['entities']
            training_example = (text, {"entities": entities})
            training_data.append(training_example)

    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(training_data, json_file, ensure_ascii=False, indent=2)


convert_jsonl_to_spacy_json('data/annotated/processed/train_items.jsonl', 'data/annotated/processed/train_items.json')
convert_jsonl_to_spacy_json('data/annotated/processed/train_context.jsonl', 'data/annotated/processed/train_context.jsonl')


def convert_json_to_spacy_docs(nlp, input_json_file):
    # Load the training data
    with open(input_json_file, 'r', encoding='utf-8') as json_file:
        training_data = json.load(json_file)

    # Create a DocBin instance to store the Doc objects
    doc_bin = DocBin(attrs=["LEMMA", "ENT_IOB", "ENT_TYPE"], store_user_data=True)

    # Convert each training example into a Doc object and add it to the DocBin
    for text, annotations in training_data:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annotations['entities']:
            span = doc.char_span(start, end, label=label)
            if span is not None:
                ents.append(span)
        doc.ents = ents
        doc_bin.add(doc)

    # Return the DocBin instance containing all Doc objects
    return doc_bin


# Load your trained or base NLP model
nlp = spacy.load("nb_core_news_sm")

# Convert your JSON training data into SpaCy Doc objects
doc_bin = convert_json_to_spacy_docs(nlp, s)

# Optionally, save your DocBin to a file for later use
doc_bin.to_disk("path/to/your/docs.spacy")
