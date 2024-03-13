import spacy
from spacy.training import Example
import pandas as pd
from tqdm import tqdm

nlp = spacy.blank("nb")  # Opprett en ny norsk spaCy-pakket
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
ner.add_label("GJENSTAND")
ner.add_label("KATEGORI")

def prepare_training_data_from_csv(csv_file_path, entity_label):
    data = pd.read_csv(csv_file_path)
    training_data = []

    for _, row in data.iterrows():
        if entity_label == "GJENSTAND":
            text = row['gjenstandbeskrivelse']  # Oppdater til korrekt kolonnenavn for gjenstander
        elif entity_label == "KATEGORI":
            text = row['kategoribeskrivelse']  # Oppdater til korrekt kolonnenavn for kategorier
        else:
            continue  # Hopper over hvis etiketten ikke er gjenkjent

        # Her tar vi en enkel tilnærming og antar at hele teksten beskriver entiteten
        start = 0
        end = len(text)
        training_data.append((text, {"entities": [(start, end, entity_label)]}))

    return training_data

kategori_training_data = prepare_training_data_from_csv("data/preprocessed_aggregated_kategori_data.csv", "KATEGORI")
gjenstand_training_data = prepare_training_data_from_csv("data/preprocessed_aggregated_gjenstand_data.csv", "GJENSTAND")
combined_training_data = kategori_training_data + gjenstand_training_data

# Konverter treningsdata til spaCy's Example-objekter
examples = []
for text, annotations in combined_training_data:
    doc = nlp.make_doc(text)
    examples.append(Example.from_dict(doc, annotations))

# Tren modellen
nlp.initialize()
for i in range(10):
    losses = {}
    # Her oppdaterer vi modellen direkte med eksemplene
    nlp.update(examples, drop=0.5, losses=losses)
    print(f"Iterasjon {i}, Losses: {losses}")

nlp.to_disk("Models/NER_Model/ner_model")
print("Modellen er trent og lagret.")


