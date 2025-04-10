import json

files = ['dataset/merged_GUA.json','dataset/merged_CBS.json','dataset/merged_JTN.json','dataset/merged_TPM.json']
bias_labels = ['left','lean-left','lean-right','right']

labelled_articles = []

for i,file_path in enumerate(files):
  with open(file_path, 'r', encoding='utf-8') as file:
    articles = json.load(file)
    for article in articles:
      labelled_articles.append({
        'article': article,
        'label': bias_labels[i]
      })
    
with open('dataset/new_test_dataset.json', 'w') as output:
  json.dump(labelled_articles, output, indent=4)

print("success")