import json


def load_data(file_path):
    TRAIN_DATA = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            text = data['text']
            entities = []
            for entity in data['entities']:
                entities.append((entity['start_offset'], entity['end_offset'], entity['label']))
            TRAIN_DATA.append((text, {"entities": entities}))
    return TRAIN_DATA


def save_data_to_file(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for text, entity_info in data:
            formatted_data = {
                "text": text,
                "entities": [list(entity) for entity in entity_info["entities"]]
            }
            json.dump(formatted_data, f, ensure_ascii=False)
            f.write('\n')  # Legger til en ny linje for hver dataenhet


TRAIN_DATA = load_data("../data/annotated/preprocessed/all2.jsonl")

# Spesifiser stien der vi vil lagre de transformerte treningsdataene
output_file_path = "../data/annotated/processed/train_items.jsonl"
save_data_to_file(TRAIN_DATA, output_file_path)
