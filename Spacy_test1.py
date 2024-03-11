import pandas as pd
import json
import spacy
from spacy.matcher import Matcher

# Load the Norwegian language model
nlp = spacy.load("nb_core_news_sm", disable=["parser", "ner"])

# Initialize the Matcher with the shared vocabulary
matcher = Matcher(nlp.vocab)

# Define the pattern that looks for phrases indicating interest in item rules
pattern = [{"LOWER": "reglene"}, {"LOWER": "for"}, {"POS": "NOUN", "OP": "+"}]
matcher.add("ITEM_QUERY", [pattern])

data_path = "data/preprocessed_aggregated_combined_data.csv"
data = pd.read_csv(data_path)
data['gjenstandnavn'] = data['gjenstandnavn'].str.lower().fillna('')


def extract_keywords_with_context(doc):
    keywords = []
    matches = matcher(doc)
    for _, start, end in matches:
        span = doc[start:end]  # The matched span
        for token in span:
            if token.pos_ == "NOUN":
                keywords.append(token.text.lower())
    return keywords


def fetch_information(item_name):
    item_info = data[data['gjenstandnavn'].str.contains(item_name, na=False)].copy()
    if item_info.empty:
        return pd.DataFrame()  # Return an empty DataFrame for consistency
    item_info.loc[:, 'rules'] = item_info['rules'].apply(lambda x: json.loads(x) if pd.notnull(x) else [])
    return item_info


def process_query(query):
    doc = nlp(query)
    keywords = extract_keywords_with_context(doc)
    if not keywords:
        return "Ingen nøkkelord funnet i forespørselen."

    all_info_collected = []
    for item_name in keywords:
        info = fetch_information(item_name)
        if not info.empty:
            all_info_collected.append(info)

    if all_info_collected:
        # Concatenate all collected dataframes
        all_info_df = pd.concat(all_info_collected).reset_index(drop=True)
        # Manually handle deduplication if necessary, considering 'rules' are lists
        return all_info_df.drop_duplicates(subset=['gjenstandnavn'])
    else:
        return "Ingen informasjon funnet for gitt(e) nøkkelord."


def display_info(info):
    if isinstance(info, pd.DataFrame) and not info.empty:
        for index, row in info.iterrows():
            print(f"Gjenstand: {row['gjenstandnavn']}")
            for rule in row['rules']:
                print(f"Betingelse: {rule['betingelse']}")
                print(f"Verdi: {rule['verdi']}")
                print(f"Tillat i Håndbagasje: {rule['tillatthandbagasje']}")
                print(f"Tillat i Innsjekket Bagasje: {rule['tillattinnsjekketbagasje']}")
                print(f"Regel: {rule.get('regelverkbeskrivelse', 'Ingen beskrivelse')}")
            print("\n")
    else:
        print(info)


# Example usage
query = "Hva er reglene for vann og balsam?"
info = process_query(query)
display_info(info)
