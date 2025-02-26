import json

files = ['dataset/merged_ATL.json','dataset/merged_BRT.json','dataset/merged_DC.json','dataset/merged_NYP.json','dataset/merged_NYT.json','dataset/merged_UST.json','dataset/merged_VOX.json','dataset/merged_WT.json']
bias_labels = ['left','right','right','lean-right','lean-left','lean-left','left','lean-right']

labelled_articles = []

for i,file_path in enumerate(files):
  with open(file_path, 'r', encoding='utf-8') as file:
    articles = json.load(file)
    for article in articles:
      labelled_articles.append({
        'article': article,
        'label': bias_labels[i]
      })
    
with open('dataset/dataset.json', 'w') as output:
  json.dump(labelled_articles, output, indent=4)

print("success")