import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
daylinks=[
  "https://web.archive.org/web/20231101004145/https://justthenews.com/politics-policy",
  "https://web.archive.org/web/20231031161227/https://justthenews.com/politics-policy",
  "https://web.archive.org/web/20231023041932/https://justthenews.com/politics-policy",
  "https://web.archive.org/web/20231010114600/https://justthenews.com/politics-policy",
  "https://web.archive.org/web/20231003000019/https://justthenews.com/politics-policy",
  "https://web.archive.org/web/20231001160554/https://justthenews.com/politics-policy",
  "https://web.archive.org/web/20230927094325/https://justthenews.com/politics-policy",
  "https://web.archive.org/web/20230925021518/https://justthenews.com/politics-policy",
  "https://web.archive.org/web/20230916000137/https://justthenews.com/politics-policy",
  "https://web.archive.org/web/20230908173225/https://justthenews.com/politics-policy"
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
  politicnews = list(set(politicnews))
  # politicnews = [link for link in politicnews if 'pages/' not in link]
  politicnews = [link for link in politicnews if '/podcasts/' not in link]
  politicnews = [link for link in politicnews if '/accountability/' not in link]
  politicnews = [link[20:] for link in politicnews]
  politicnews = [link for link in politicnews if len(link)>=60]
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

with open('dataset/JTN/jtn-partthree.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)