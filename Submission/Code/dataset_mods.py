import json
import re

with open("dataset/merged_TPM.json","r",encoding="utf-8") as f:
  data = json.load(f)

unwanted_text_end = ""
unwanted_text_start = "2023-"
unwanted_text = "POLL DU JOUR"

def clean_article(text):
  lower_text = text.lower()

  index = lower_text.find(unwanted_text_start)
  if index!=-1:
    return text[:index].strip()
  
  # index = lower_text.find(unwanted_text_end)
  # if index!=-1:
  #   return text[index + len(unwanted_text_end):].strip()

  #text = text.replace(unwanted_text,"").strip()
  
  #text =re.sub(r'^Supreme Court ','',text)

  return text

def remove_dups(data):
  seen = set()
  cleaned = []
  for text in data:
    if text not in seen:
      seen.add(text)
      cleaned.append(text)
  return cleaned

def remove_empties(data):
  cleaned = []
  for text in data:
    if len(text)>1:
      cleaned.append(text)
  return cleaned

def stupiddup(data):
  cleaned = []
  for text in data:
    splits = text.split(". ")
    if len(splits) > 1:
      if (splits[0] == splits[1]) and (len(splits)==2):
        continue
    splits = text.split('." ')
    if len(splits) > 1:
      if (splits[0] == splits[1]) and (len(splits)==2):
        continue
    cleaned.append(text)
  return cleaned


# for entry in data:
#   entry = clean_article(entry)
#   entry["article"] = clean_article(entry["article"])

# data = [clean_article(text) for text in data]
# data = remove_dups(data)
# data = remove_empties(data)
# data = stupiddup(data)
data = [item for item in data if len(item)>=2385]

with open("dataset/merged_TPM.json","w",encoding="utf-8") as f:
  json.dump(data, f, ensure_ascii=False, indent=4)

print("done")