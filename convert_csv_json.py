import os
import csv
import json
import re

# Define input and output directories
input_folder = "dataset/NYP"
output_folder = "dataset/NYP"
os.makedirs(output_folder, exist_ok=True)

# Loop through all CSV files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename.replace(".csv", ".json"))

        # Read CSV file
        articles = []
        with open(input_file_path, mode="r", encoding="utf-8", errors="ignore") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row:  # Ignore empty rows
                    articles.append(row[0])  # Assuming articles are in the first column


        # Write to JSON file
        with open(output_file_path, mode="w", encoding="utf-8", errors="ignore") as json_file:
            json.dump(articles, json_file, indent=4)

        print(f"Converted {filename} to {output_file_path}")

        with open(output_file_path, mode="r", encoding="utf-8") as json_file:
            json_data = json_file.read()

        # Use regex to remove \uXXXX patterns
        cleaned_data = re.sub(r'\\u[0-9a-fA-F]{4}', '', json_data)

        # Write the cleaned data back to the file
        with open(output_file_path, mode="w", encoding="utf-8") as json_file:
            json_file.write(cleaned_data)

        print(f"Converted and cleaned {filename} to {output_file_path}")