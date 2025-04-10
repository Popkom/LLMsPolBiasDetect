import os
import json

input_dir = 'dataset/JTN'
output_file = 'dataset/merged_JTN.json'

all_strings = []

for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        filepath = os.path.join(input_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    all_strings.extend(data)
                else:
                    print(f"Skipping file {filename} as it does not contain a JSON array.")
            except json.JSONDecodeError:
                print(f"Skipping file {filename} due to JSON decoding error.")

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_strings, f, ensure_ascii=False, indent=2)

print(f"Merged {len(all_strings)} strings into {output_file}.")