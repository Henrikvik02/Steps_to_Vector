import spacy
import json

def generate_questions(item):
    """Generate simple questions for a given item."""
    questions = [
        f"Kan jeg ta med {item} på flyet?"
    ]
    return questions

def get_user_feedback(predicted_entity, item):
    """Prompt the user for feedback on the model's prediction."""
    response = input(f"Is '{predicted_entity}' correctly identified as 'Gjenstand' for item '{item}'? (y/n): ").strip().lower()
    return response == 'y'

def test_model_with_items(jsonl_file_path, model_path="./output/model-best", results_file="evaluation_results.txt"):
    """Test a spaCy model with generated questions for each item and collect user feedback."""
    nlp = spacy.load(model_path)
    results = []

    with open(jsonl_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line_data = json.loads(line)
            item = line_data['text']
            for question in generate_questions(item):
                doc = nlp(question)
                print(f"\nQuestion: {question}")
                if doc.ents:
                    for ent in doc.ents:
                        print(f"Predicted entity: {ent.text} ({ent.label_})")
                        correct = get_user_feedback(ent.text, item)
                        results.append({'item': item, 'question': question, 'predicted_entity': ent.text, 'correct': correct})
                else:
                    print("No entities predicted.")
                    results.append({'item': item, 'question': question, 'predicted_entity': None, 'correct': None})

    # Save the results to a file
    with open(results_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')
    print(f"\nEvaluation results saved to {results_file}")

# Example usage
jsonl_file_path = './data/annotated/processed/train_items.jsonl'  # Update this path
test_model_with_items(jsonl_file_path)
