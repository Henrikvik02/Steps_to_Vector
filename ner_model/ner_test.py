import spacy

# Last inn den tilpassede modellen ved navn
nlp = spacy.load("nb_min_modell")

# Behandle eksempelteksten med modellen
test_doc = nlp("Kan jeg ta med rullestol på flyet?")

# Skriv ut gjenkjente entiteter og deres etiketter
for ent in test_doc.ents:
    print(f"{ent.text}: {ent.label_}")
