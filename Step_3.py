import json
import pandas as pd

import spacy

# Load spaCy's Norwegian model
nlp = spacy.load("nb_core_news_sm")

# Load the combined data
csv_file_path = "data/combined_data.csv"
data = pd.read_csv(csv_file_path, encoding='utf-8')

def preprocess_text(text):
    # Return empty string if text is not a string
    if not isinstance(text, str):
        return ''

    # Initialize a spaCy document
    doc = nlp(text.lower())

    # Lemmatize and remove stop words and punctuation
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

    # Join lemmatized tokens back into a single string
    return ' '.join(lemmatized_tokens)


def format_lovverk(df):
    rules = [{
        'betingelse': preprocess_text(rule['betingelse']),
        'verdi': preprocess_text(rule['verdi']),
        'tillatthandbagasje': preprocess_text(str(rule['tillatthandbagasje'])),
        'tillattinnsjekketbagasje': preprocess_text(str(rule['tillattinnsjekketbagasje'])),
        'regelverkbeskrivelse': preprocess_text(rule['regelverkbeskrivelse'])
    } for rule in df.to_dict('records')]

    # Ensure ASCII is False to handle Norwegian characters
    return json.dumps(rules, ensure_ascii=False)

def generate_aggregated_data():
    aggregated_data = data.groupby(['gjenstandnavn', 'kategorinavn']).apply(lambda df: pd.Series({
        'gjenstandbeskrivelse': preprocess_text(df['gjenstandbeskrivelse'].iloc[0]),
        'kategoribeskrivelse': preprocess_text(df['kategoribeskrivelse'].iloc[0]),
        'lovverk': format_lovverk(df)
    })).reset_index()
    preprocessed_aggregated_file_path = "data/aggregated/preprocessed_aggregated_combined_data.csv"
    aggregated_data.to_csv(preprocessed_aggregated_file_path, index=False, encoding='utf-8')
    print("aggregated data saved to:", preprocessed_aggregated_file_path)
    return aggregated_data

def generate_lovverk_data(aggregated_data):
    lovverk_data = aggregated_data[['lovverk']].drop_duplicates().reset_index(drop=True)
    lovverk_data_file_path = "data/aggregated/preprocessed_aggregated_lovverk_data.csv"
    lovverk_data.to_csv(lovverk_data_file_path, index=False, encoding='utf-8')
    print(f"Rules data saved to {lovverk_data_file_path}")
def generate_gjenstand_data(aggregated_data):
    gjenstand_data = aggregated_data[['gjenstandnavn']].drop_duplicates().reset_index(drop=True)
    gjenstand_file_path = "data/aggregated/preprocessed_aggregated_gjenstand_data.csv"
    gjenstand_data.to_csv(gjenstand_file_path, index=False, encoding='utf-8')
    print(f"Item data saved to {gjenstand_file_path}")

# Function to generate item data files
def generate_gjenstand_med_forklaring_data(aggregated_data):
    gjenstand_med_forklaring_data = aggregated_data[['gjenstandnavn', 'gjenstandbeskrivelse']].drop_duplicates().reset_index(drop=True)
    gjenstand_med_forklaring_file_path = "data/aggregated/preprocessed_aggregated_gjenstand_med_beskrivelse_data.csv"
    gjenstand_med_forklaring_data.to_csv(gjenstand_med_forklaring_file_path, index=False, encoding='utf-8')
    print(f"Item with explanation data saved to {gjenstand_med_forklaring_file_path}")

def generate_gjenstand_med_lovverk_data(aggregated_data):
    gjenstand_med_lovverk_data = aggregated_data[['gjenstandnavn', 'lovverk']].drop_duplicates().reset_index(drop=True)
    gjenstand_med_lovverk_file_path = "data/aggregated/preprocessed_aggregated_gjenstand_med_lovverk_data.csv"
    gjenstand_med_lovverk_data.to_csv(gjenstand_med_lovverk_file_path, index=False, encoding='utf-8')
    print(f"Item with rules data saved to {gjenstand_med_lovverk_file_path}")

def generate_kategori_data(aggregated_data):
    kategori_data = aggregated_data[['kategorinavn']].drop_duplicates().reset_index(drop=True)
    kategori_file_path = "data/aggregated/preprocessed_aggregated_kategori_data.csv"
    kategori_data.to_csv(kategori_file_path, index=False, encoding='utf-8')
    print(f"Category data saved to {kategori_file_path}")

# Function to generate category data files
def generate_kategori_med_forklaring_data(aggregated_data):
    kategori_med_forklaring_data = aggregated_data[['kategorinavn', 'kategoribeskrivelse']].drop_duplicates().reset_index(drop=True)
    kategori_med_forklaring_file_path = "data/aggregated/preprocessed_aggregated_kategori_med_forklaring_data.csv"
    kategori_med_forklaring_data.to_csv(kategori_med_forklaring_file_path, index=False, encoding='utf-8')
    print(f"Category with explanation data saved to {kategori_med_forklaring_file_path}")

def generate_kategori_med_lovverk_data(aggregated_data):
    # Anta at 'aggregated_data' allerede inneholder en kolonne 'rules' som er en JSON-streng av regler
    # Hvis 'aggregated_data' ikke har denne strukturen, må du justere tilnærmingen tilsvarende
    kategori_med_lovverk_data = aggregated_data[['kategorinavn', 'lovverk']].drop_duplicates().reset_index(drop=True)
    kategori_med_lovverk_file_path = "data/aggregated/preprocessed_aggregated_kategori_med_lovverk_data.csv"
    kategori_med_lovverk_data.to_csv(kategori_med_lovverk_file_path, index=False, encoding='utf-8')
    print(f"Category with rules data saved to {kategori_med_lovverk_file_path}")

def generate_kategori_med_gjenstander_data(aggregated_data):
    # For å aggregere gjenstander per kategori i JSON-format, kan det være nødvendig
    # å forenkle eller justere denne funksjonen basert på dine faktiske data.
    # Dette eksemplet antar en tilnærming hvor vi kun lister opp gjenstandnavn under hver kategori.
    kategori_med_gjenstander = aggregated_data.groupby('kategorinavn')['gjenstandnavn'].unique().reset_index()
    kategori_med_gjenstander['gjenstandnavn'] = kategori_med_gjenstander['gjenstandnavn'].apply(
        lambda x: json.dumps(list(x)))

    kategori_med_gjenstander_file_path = "data/aggregated/preprocessed_aggregated_kategori_med_gjenstander_data.csv"
    kategori_med_gjenstander.to_csv(kategori_med_gjenstander_file_path, index=False, encoding='utf-8')
    print(f"Category with Items data saved to {kategori_med_gjenstander_file_path}")


# Call the function to generate combined data
aggregated_data = generate_aggregated_data()
generate_lovverk_data(aggregated_data)
generate_gjenstand_data(aggregated_data)
generate_gjenstand_med_forklaring_data(aggregated_data)
generate_gjenstand_med_lovverk_data(aggregated_data)
generate_kategori_data(aggregated_data)
generate_kategori_med_forklaring_data(aggregated_data)
generate_kategori_med_lovverk_data(aggregated_data)
generate_kategori_med_gjenstander_data(aggregated_data)