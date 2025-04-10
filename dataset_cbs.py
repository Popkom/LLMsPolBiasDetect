import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
daylinks=[
  "https://web.archive.org/web/20240630164437/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240628132745/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240626103748/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240624091806/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240622053802/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240620204405/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240618232127/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240616235452/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240614214043/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240612233204/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240610175030/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240608225124/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240606210524/https://www.cbsnews.com/politics/",
  "https://web.archive.org/web/20240604193117/https://www.cbsnews.com/politics/"
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
  politicnews = [link for link in politicnews if '/news/' in link]
  politicnews = [link for link in politicnews if 'cbsnews' in link]
  politicnews = politicnews[:15]
  politicnews = [link[43:] for link in politicnews]
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

with open('dataset/CBS/cbs-jun-2024.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)