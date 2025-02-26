import requests
import json
import time
from bs4 import BeautifulSoup
import cfscrape
import csv

year = 2023
month = 9
nyt_url = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key=4XGBBGOkF50iHE7zQ7C17DGd6NPYJ6R7"
response = requests.get(nyt_url)
data = response.json()
articleswithunwanted = data["response"]["docs"]
articles = []
for a in articleswithunwanted:
  if "Siena" in a["abstract"]:
    continue
  articles.append(a)
pol_articles = []
texts = []
scraper = cfscrape.create_scraper()
i = 0
for article in articles:
  try:
    if(article['section_name']=="U.S."):
      if(article['subsection_name'] == "Politics"):
        #print(i)
        if i == 162:
          continue
        pol_articles.append(article)
        article_url = article["web_url"]
        session = requests.Session()
        req = scraper.get(article_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ""
        if "A PDF version of this document with embedded text is available at the link below:" in paragraphs[1]:
          continue
        if len(paragraphs) > 1:
          #print(paragraphs)
          for p in paragraphs:
            text = text + " " + p.get_text()
            text = text.replace('Advertisement','')
            text = text.replace('New York Times','')
          #print(text)
          texts.append(text)
          i = i +1
        else:
          #print(paragraphs)
          i= i+1
  except:
    i = i + 1
    continue

# print(len(texts))
# print(texts[200])
# print(texts[199])

with open('dataset/nytimes.csv', 'w',encoding='utf-8', newline='') as nyt:
  wr = csv.writer(nyt)
  for text in texts:
    wr.writerow([text])