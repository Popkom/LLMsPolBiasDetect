import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
daylinks=[
  "https://web.archive.org/web/20240518000516/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240516193910/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240515064510/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240512172936/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240501190607/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240410140018/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240404171237/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240401064409/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240325204112/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240324235345/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240303235304/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240227042458/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240202125139/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240201054509/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20240101061652/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20231206112804/https://thepostmillennial.com/news",
  "https://web.archive.org/web/20231201142858/https://thepostmillennial.com/news"
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
  # politicnews = politicnews[114:124]
  politicnews = [link for link in politicnews if 'pages/' not in link]
  politicnews = [link for link in politicnews if '/support-independent' not in link]
  politicnews = [link for link in politicnews if '/page/' not in link]
  politicnews = [link for link in politicnews if len(link)>=75]
  politicnews = list(set(politicnews))
  politicnews = [link[20:] for link in politicnews]
  politicnews = [link for link in politicnews if 'org/' not in link]
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

with open('dataset/TPM/tpm-parttwo.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)