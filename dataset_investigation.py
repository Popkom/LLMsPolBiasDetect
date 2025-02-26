import json
import re
from collections import Counter
from itertools import islice

with open("dataset/merged_WT.json","r", encoding="utf-8") as f:
  data = json.load(f)

def get_trigrams(text):
  words = re.findall(r'\b\w+\b', text.lower())
  return [" ".join(words[i:i+5]) for i in range(len(words)-2)]

trigram_counter = Counter()

for entry in data:
  trigrams = get_trigrams(entry)
  trigram_counter.update(trigrams)

most_common_trigrams = trigram_counter.most_common(40)

for trigram, count in most_common_trigrams:
  print(f"{trigram}: {count}")