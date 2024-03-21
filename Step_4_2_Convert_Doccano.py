import json


def Convert_Doccano_to_SpacyJsonl(input_file_path, output_file_path):
    """
    Converts data from Doccano JSONL format to spaCy JSONL format.

    Parameters:
    input_file_path (str): The path to the input JSONL file.
    output_file_path (str): The path to the output JSONL file.
    """
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file:

        for line in input_file:
            # Load the JSON object from each line of the input file
            data = json.loads(line)

            # Prepare the text from the JSON object
            text = data["text"]

            # Prepare the entities list in the format (start, end, label)
            entities = []
            for entity in data["entities"]:
                start_offset = entity["start_offset"]
                end_offset = entity["end_offset"]
                label = entity["label"]
                entities.append((start_offset, end_offset, label))

            # Format the text and entities for spaCy
            spacy_format = (text, {"entities": entities})

            # Convert the tuple to JSONL and write to the output file
            output_file.write(json.dumps(spacy_format, ensure_ascii=False) + '\n')


def convert_format(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            data = json.loads(line)  # Load JSON object from line
            text = data["text"]
            entities = data["entities"]

            # Prepare the target format
            converted_line = json.dumps([text, {"entities": entities}], ensure_ascii=False)

            # Write the converted line to output file
            output_file.write(converted_line + '\n')


# Example usage
input_file_path = 'data/annotated/processed/train_items.jsonl'
output_file_path = 'data/annotated/processed/train_items2.jsonl'
convert_format(input_file_path, output_file_path)
