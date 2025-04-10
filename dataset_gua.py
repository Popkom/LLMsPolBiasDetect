import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
daylinks=[
  "https://web.archive.org/web/20230930142005/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230928183752/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230926210603/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230924224101/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230922234925/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230920222951/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230918203410/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230916193215/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230914202725/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230912192237/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230910165707/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230908182227/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230906124330/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230904231412/https://www.theguardian.com/us-news/us-politics",
  "https://web.archive.org/web/20230902185806/https://www.theguardian.com/us-news/us-politics"
          ]

totallinks=[]
for link in daylinks:
  req = Request(
      url=link, 
      headers={'User-Agent': 'Mozilla/5.0'}
  )
  try:
    page = urlopen(req).read()
  except http.client.IncompleteRead as e:
    page = e.partial
  soup = BeautifulSoup(page, 'html.parser')
  atags = soup.find_all('a')
  links = [atag.get('href') for atag in atags]
  politicnews = links
  politicnews = [link for link in politicnews if link is not None]
  politicnews = politicnews[114:124]
  politicnews = [link for link in politicnews if '/audio/' not in link]
  politicnews = [link for link in politicnews if '/live/' not in link]
  politicnews = [link for link in politicnews if '/all' not in link]
  politicnews = [link for link in politicnews if '/us-news/2023' in link]
  politicnews = [link[20:] for link in politicnews]
  for l in politicnews:
    print(l)
  for link in politicnews:
    if link.startswith("https"):
      totallinks.append(link)
  time.sleep(2)

totallinks = list(set(totallinks))

texts = []
for link in totallinks:
  req = Request(
      url=link, 
      headers={'User-Agent': 'Mozilla/5.0'}
  )
  try:
    page = urlopen(req).read()
  except Exception as e:
    print(e)
    continue
  soup = BeautifulSoup(page, 'html.parser')
  paragraphs = soup.find_all('p')
  text = ""
  for p in paragraphs:
    text = text + " " + p.get_text()
    
  #print(text)
  texts.append(text)
  time.sleep(1.5)

print(len(texts))

with open('dataset/GUA/guardian-sep-2023.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)