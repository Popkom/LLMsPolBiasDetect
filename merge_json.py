import os
import json

# Directory containing the JSON files
input_dir = 'dataset/WT'
output_file = 'dataset/merged_WT.json'

# Initialize an empty list to hold all strings
all_strings = []

# Iterate through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        filepath = os.path.join(input_dir, filename)
        
        # Open and read each JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    all_strings.extend(data)  # Add strings to the list
                else:
                    print(f"Skipping file {filename} as it does not contain a JSON array.")
            except json.JSONDecodeError:
                print(f"Skipping file {filename} due to JSON decoding error.")

# Write the merged list of strings to the output file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_strings, f, ensure_ascii=False, indent=2)

print(f"Merged {len(all_strings)} strings into {output_file}.")