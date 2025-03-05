import json
import re

with open("dataset/dataset.json","r",encoding="utf-8") as f:
  data = json.load(f)

unwanted_text_end = "inbox each sunday"
unwanted_text_start = "follow brianna"
unwanted_text = "POLL DU JOUR"

def clean_article(text):
  lower_text = text.lower()

  # index = lower_text.find(unwanted_text_start)
  # if index!=-1:
  #   return text[:index].strip()
  
  # index = lower_text.find(unwanted_text_end)
  # if index!=-1:
  #   return text[index + len(unwanted_text_end):].strip()

  #text = text.replace(unwanted_text,"").strip()
  
  text =re.sub(r'^Supreme Court ','',text)

  return text

def remove_dups(data):
  seen = set()
  cleaned = []
  for text in data:
    if text not in seen:
      seen.add(text)
      cleaned.append(text)
  return cleaned

for entry in data:
  #entry = clean_article(entry)
  entry["article"] = clean_article(entry["article"])

# cleaned_data = [clean_article(text) for text in data]
# cleaned_data = remove_dups(data)

with open("dataset/dataset.json","w",encoding="utf-8") as f:
  json.dump(data, f, ensure_ascii=False, indent=4)

print("done")