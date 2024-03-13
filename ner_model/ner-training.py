import spacy
from spacy.training.example import Example
import random
import json

# Last inn den eksisterende modellen
nlp = spacy.load("nb_core_news_sm")

# Identifiser NER-komponenten i modellen
if "ner" not in nlp.pipe_names:
    ner = nlp.create_pipe("ner")
    nlp.add_pipe(ner)
else:
    ner = nlp.get_pipe("ner")

# Legg til den nye entitetsetiketten til NER-komponenten
ner.add_label("Gjenstand")

# Få listen av andre komponenter for å kunne deaktivere dem under trening
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        TRAIN_DATA = []
        for line in file:
            data = json.loads(line)
            text = data['text']
            entities = data['entities']
            TRAIN_DATA.append((text, {"entities": entities}))
    return TRAIN_DATA

TRAIN_DATA = load_data('../data/annotated/processed/train_items.jsonl')

# Trening av modellen
with nlp.disable_pipes(*other_pipes):  # Deaktiver andre komponenter
    optimizer = nlp.begin_training()
    i = 0
    for itn in range(300):  # Antall iterasjoner
        i+1
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            i+1
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses)
        print(i, "Tap:", losses)

nlp.to_disk("oppdatert_norsk_modell")
