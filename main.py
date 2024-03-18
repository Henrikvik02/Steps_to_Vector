import json

def convert_jsonl_format(input_file_path, output_file_path):
    # Open the input JSONL file and read line by line
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # Open the output JSONL file for writing the modified content
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in lines:
            data = json.loads(line)
            # Modify the format of each JSON object
            new_data = {
                "text": data["text"],
                "label": []  # Set 'label' to an empty list as required
            }
            # Write the modified JSON object to the output file
            output_file.write(json.dumps(new_data, ensure_ascii=False) + '\n')

# Example usage
input_file_path = 'data/annotated/processed/train_context.jsonl'
output_file_path = 'data/preprocessed/jsonl/train_context.jsonl'
convert_jsonl_format(input_file_path, output_file_path)
