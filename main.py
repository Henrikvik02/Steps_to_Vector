import spacy

# Load your chosen model (replace "model-best" with "model-last" if you decide to use that)
nlp = spacy.load("./output/model-last")

# Process text with the model
doc = nlp("Kan jeg ta med meg en rullestol?")
for ent in doc.ents:
    print(ent.text, ent.label_)