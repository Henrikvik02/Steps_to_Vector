import json
import os
import spacy

# Last inn spaCy's norske pakket
nlp = spacy.load("nb_core_news_sm")


# Funksjon for å laste inn data fra en JSON-fil
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Funksjon for å forbehandle tekst
# Unngår lemmatisering for alt er allerede definert godt i relasjonsdatabasen,
# vi vil nemlig at den bare skal hente ut data relatert.
def preprocess_text(text):
    if not isinstance(text, str):
        return ''

    doc = nlp(text.lower())

    # Behold ordene som de er uten lemmatisering, men fjern stoppord og tegnsetting
    filtered_tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]

    return ' '.join(filtered_tokens)


# Funksjon for å forbehandle og lagre data
def preprocess_and_save_data(input_file_path, output_file_path):
    data = load_data_from_json(input_file_path)

    # Forbehandle hver tekststreng i datasettet
    preprocessed_data = []
    for item in data:
        preprocessed_item = {key: preprocess_text(value) if isinstance(value, str) else value for key, value in
                             item.items()}
        preprocessed_data.append(preprocessed_item)

    # Lagre forbehandlet data tilbake til JSON
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(preprocessed_data, f, ensure_ascii=False, indent=4)

    print(f"Preprocessed data saved to: {output_file_path}")


# Spesifiser stier for inndata og utdatafiler
input_files_and_output_paths = [
    ("data/fetched/combined_data.json", "data/preprocessed/json/combined_data.json"),
    ("data/fetched/kategorier.json", "data/preprocessed/json/kategorier.json"),
    ("data/fetched/regelverker.json", "data/preprocessed/json/regelverker.json"),
    ("data/fetched/gjenstander.json", "data/preprocessed/json/gjenstander.json"),
    ("data/fetched/regelverktag.json", "data/preprocessed/json/regelverktag.json")
]

# Utfør forbehandling for hver fil
for input_path, output_path in input_files_and_output_paths:
    preprocess_and_save_data(input_path, output_path)


# Hjelpefunksjon for å lagre data til JSON
def save_data_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 1. Gjenstander
def generate_gjenstander_med_navn_file(input_file_path, output_file_path):
    data = load_data_from_json(input_file_path)

    # Filtrer ut kun gjenstandnavn
    items_only_data = [{'gjenstandnavn': item['gjenstandnavn']} for item in data]

    # Lagre filtrerte data tilbake til JSON
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(items_only_data, f, ensure_ascii=False, indent=4)

    print(f"Items only data saved to: {output_file_path}")


# 2. Gjenstander med beskrivelse
def generate_gjenstander_med_beskrivelse_file(input_file_path, output_file_path):
    data = load_data_from_json(input_file_path)

    # Filtrer ut gjenstandnavn og tilhørende beskrivelse
    gjenstander_med_beskrivelse_data = [
        {
            'gjenstandnavn': item['gjenstandnavn'],
            'gjenstandbeskrivelse': item['gjenstandbeskrivelse']
        }
        for item in data if 'gjenstandbeskrivelse' in item
        # Sørger for at vi kun inkluderer items som har en beskrivelse
    ]

    # Lagre filtrerte data tilbake til JSON
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(gjenstander_med_beskrivelse_data, f, ensure_ascii=False, indent=4)

    print(f"Gjenstander med beskrivelse data lagret i: {output_file_path}")


# 3. Gjenstander med regelverker
def generate_gjenstander_med_regelverk_file(input_file_path, output_file_path):
    """Genererer en fil for gjenstander med tilhørende alle relevante lovverk som array."""
    data = load_data_from_json(input_file_path)

    gjenstander_med_regelverk = {}

    for item in data:
        gjenstand_navn = item['gjenstandnavn']
        if gjenstand_navn not in gjenstander_med_regelverk:
            gjenstander_med_regelverk[gjenstand_navn] = {
                'gjenstandnavn': gjenstand_navn,
                'gjenstandbeskrivelse': item.get('gjenstandbeskrivelse', ''),
                'regelverker': []
            }

        regelverk = {
            'betingelse': item.get('betingelse', ''),
            'verdi': item.get('verdi', ''),
            'tillatthandbagasje': item.get('tillatthandbagasje', False),
            'tillattinnsjekketbagasje': item.get('tillattinnsjekketbagasje', False),
            'regelverkbeskrivelse': item.get('regelverkbeskrivelse', '')
        }

        gjenstander_med_regelverk[gjenstand_navn]['regelverker'].append(regelverk)

    # Lagrer de aggregerte gjenstandene med tilhørende lovverk til en JSON-fil
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(list(gjenstander_med_regelverk.values()), file, ensure_ascii=False, indent=4)

    print(f"Data for gjenstander med lovverk lagret til: {output_file_path}")


# 4. Kategorier
def generate_kategorier_file(input_file_path, output_file_path):
    data = load_data_from_json(input_file_path)

    # Filtrer ut kun gjenstandnavn
    items_only_data = [{'kategorinavn': item['kategorinavn']} for item in data]

    # Lagre filtrerte data tilbake til JSON
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(items_only_data, f, ensure_ascii=False, indent=4)

    print(f"Kategori only data saved to: {output_file_path}")


# 5. Kategorier med beskrivelse
def generate_kategorier_med_beskrivelse_file(input_file_path, output_file_path):
    data = load_data_from_json(input_file_path)

    # Filtrer ut gjenstandnavn og tilhørende beskrivelse
    kategorier_med_beskrivelse_data = [
        {
            'kategorinavn': item['kategorinavn'],
            'kategoribeskrivelse': item['kategoribeskrivelse']
        }
        for item in data if 'kategoribeskrivelse' in item
        # Sørger for at vi kun inkluderer items som har en beskrivelse
    ]

    # Lagre filtrerte data tilbake til JSON
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(kategorier_med_beskrivelse_data, f, ensure_ascii=False, indent=4)

    print(f"Kategorier med beskrivelse data lagret i: {output_file_path}")


# 6 Kategorier med gjenstander
def generate_kategorier_med_gjenstander_file(input_file_path, output_file_path):
    """Genererer en fil for kategorier med tilhørende gjenstander og regelverk som array."""
    data = load_data_from_json(input_file_path)

    # Grupperer data basert på kategorinavn for å samle relaterte gjenstander og deres regelverk
    kategori_gjenstander_mapping = {}
    for item in data:
        kategori = item['kategorinavn']
        if kategori not in kategori_gjenstander_mapping:
            kategori_gjenstander_mapping[kategori] = {
                'kategorinavn': kategori,
                'kategoribeskrivelse': item['kategoribeskrivelse'],
                'gjenstander': []
            }

        gjenstand = {
            'gjenstandnavn': item['gjenstandnavn'],
            'gjenstandbeskrivelse': item.get('gjenstandbeskrivelse', ''),
            'regelverk': {
                'betingelse': item.get('betingelse', ''),
                'verdi': item.get('verdi', ''),
                'tillatthandbagasje': item.get('tillatthandbagasje', False),
                'tillattinnsjekketbagasje': item.get('tillattinnsjekketbagasje', False),
                'regelverkbeskrivelse': item.get('regelverkbeskrivelse', '')
            }
        }
        kategori_gjenstander_mapping[kategori]['gjenstander'].append(gjenstand)

    # Konverterer mappingen til en liste med kategorier og deres relaterte gjenstander inkludert regelverk
    kategorier_med_gjenstander_data = list(kategori_gjenstander_mapping.values())

    # Lagrer den aggregerte listen av kategorier med tilhørende gjenstander og regelverk til en JSON-fil
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(kategorier_med_gjenstander_data, file, ensure_ascii=False, indent=4)

    print(f"Data for kategorier med gjenstander og deres regelverk lagret til: {output_file_path}")


# 7. Kategorier med regelverk
def generate_kategorier_med_regelverk_file(input_file_path, output_file_path):
    """Genererer en fil for kategorier med tilhørende regelverk som array."""
    data = load_data_from_json(input_file_path)

    # Grupperer data basert på kategorinavn for å samle relaterte regelverk
    kategori_regelverk_mapping = {}
    for item in data:
        kategori = item['kategorinavn']
        if kategori not in kategori_regelverk_mapping:
            kategori_regelverk_mapping[kategori] = {
                'kategorinavn': kategori,
                'kategoribeskrivelse': item['kategoribeskrivelse'],
                'regelverk': []
            }

        regelverk = {
            'betingelse': item.get('betingelse', ''),
            'verdi': item.get('verdi', ''),
            'tillatthandbagasje': item.get('tillatthandbagasje', False),
            'tillattinnsjekketbagasje': item.get('tillattinnsjekketbagasje', False),
            'regelverkbeskrivelse': item.get('regelverkbeskrivelse', '')
        }
        kategori_regelverk_mapping[kategori]['regelverk'].append(regelverk)

    # Konverterer mappingen til en liste med kategorier og deres relaterte regelverk
    kategorier_med_regelverk_data = list(kategori_regelverk_mapping.values())

    # Lagrer den aggregerte listen av kategorier med tilhørende regelverk som array til en JSON-fil
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(kategorier_med_regelverk_data, file, ensure_ascii=False, indent=4)

    print(f"Data for kategorier med regelverk lagret til: {output_file_path}")


generate_gjenstander_med_navn_file("data/preprocessed/json/gjenstander.json",
                                   "data/preprocessed/json/gjenstander_navn.json")

generate_gjenstander_med_beskrivelse_file("data/preprocessed/json/gjenstander.json",
                                          "data/preprocessed/json/gjenstander_med_beskrivelse.json")

generate_gjenstander_med_regelverk_file("data/preprocessed/json/combined_data.json",
                                        "data/preprocessed/json/gjenstander_med_lovverk.json")

generate_kategorier_file("data/preprocessed/json/kategorier.json",
                         "data/preprocessed/json/kategorier_navn.json")

generate_kategorier_med_beskrivelse_file("data/preprocessed/json/kategorier.json",
                                         "data/preprocessed/json/kategorier_med_beskrivelse.json")

generate_kategorier_med_gjenstander_file("data/preprocessed/json/combined_data.json",
                                         "data/preprocessed/json/kategorier_med_gjenstander.json")

generate_kategorier_med_regelverk_file("data/preprocessed/json/combined_data.json",
                                       "data/preprocessed/json/kategorier_med_regelverk.json")


def convert_folder_json_to_jsonl_with_labels(input_folder_path, output_folder_path):
    # Sørg for at utmappen eksisterer
    os.makedirs(output_folder_path, exist_ok=True)

    # Iterer over alle filer i in-mappen
    for filename in os.listdir(input_folder_path):
        # Sjekk om filen er en JSON-fil
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, filename.replace('.json', '.jsonl'))

            # Konverter JSON-fil til JSONL og legg til en tom 'label'-kolonne
            with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
                data = json.load(input_file)
                for entry in data:
                    # Legger til en tom 'label'-kolonne til hver oppføring
                    entry_with_label = entry
                    entry_with_label['label'] = []  # Du kan tilpasse dette basert på dine behov
                    json_record = json.dumps(entry_with_label, ensure_ascii=False)
                    output_file.write(json_record + '\n')
            print(f"Konvertert {filename} til JSONL med labels og lagret i {output_file_path}")



convert_folder_json_to_jsonl_with_labels("data/preprocessed/json", "data/preprocessed/jsonl")
