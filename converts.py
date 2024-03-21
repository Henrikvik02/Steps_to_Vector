import json
import spacy
from spacy.tokens import DocBin


def convert_json_jsonl(file_path, out_file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open(out_file_path, 'w', encoding='utf-8') as jsonl_file:
        for entry in data:
            jsonl_file.write(json.dumps(entry) + '\n')


def convert_jsonl_json(file_path, out_file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            data.append(json.loads(line))

    with open(out_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def convert_jsonl_spacyjson(file_path, out_file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            entry = json.loads(line)
            text = entry["text"]
            entities = [(start, end, label) for start, end, label in entry["entities"]]
            data.append((text, {"entities": entities}))

    with open(out_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def convert_spacyjson_docs(file_path, out_file_path, lang_model="nb_core_news_lg"):
    nlp = spacy.load(lang_model)
    training_data = []
    with open(file_path, 'r', encoding='utf-8') as json_file:
        training_data = json.load(json_file)

    db = DocBin()
    for text, annotations in training_data:
        doc = nlp(text)
        ents = []
        for start, end, label in annotations["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is not None:  # Ensure the span is valid
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(out_file_path)

#import json
# from spacy.tokens import DocBin, Span


# def convert_json_to_jsonl(filepath, outfilepath):
# with open(filepath, 'r', encoding='utf-8') as json_file:
# data = json.load(json_file)

# with open(outfilepath, 'w', encoding='utf-8') as jsonl_file:
# for entry in data:
# jsonl_file.write(json.dumps(entry, ensure_ascii=False) + '\n')


# def convert_jsonl_to_json(filepath, outfilepath):
# data = []
# with open(filepath, 'r', encoding='utf-8') as jsonl_file:
# for line in jsonl_file:
# data.append(json.loads(line.strip()))

# with open(outfilepath, 'w', encoding='utf-8') as json_file:
# json.dump(data, json_file, ensure_ascii=False, indent=4)


# def convert_jsonl_to_spacyjson(filepath, outfilepath):
# data = []
# with open(filepath, 'r', encoding='utf-8') as jsonl_file:
# for line in jsonl_file:
# entry = json.loads(line.strip())
# spacy_entry = {
# "text": entry["text"],
# "ents": [{"start": ent[0], "end": ent[1], "label": ent[2]} for ent in entry.get("entities", [])],
# "title": None
# }
# data.append(spacy_entry)

# with open(outfilepath, 'w', encoding='utf-8') as json_file:
# json.dump(data, json_file, ensure_ascii=False, indent=4)


# def convert_spacyjson_to_docs(nlp, filepath, outfilepath):
# db = DocBin()  # Create a DocBin object
# with open(filepath, 'r', encoding='utf-8') as json_file:
# data = json.load(json_file)
# for entry in data:
# doc = nlp.make_doc(entry["text"])  # Create a Doc object from the text
# ents = []
# for ent in entry.get("ents", []):
# ents.append(Span(doc, ent["start"], ent["end"], label=ent["label"]))
# doc.ents = ents  # Set the entities for the Doc object
# db.add(doc)

# db.to_disk(outfilepath)  # Save the DocBin to disk

# Note: This code is for demonstration purposes. Replace 'filepath' and 'outfilepath' with your actual file paths.
