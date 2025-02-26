import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
from datetime import datetime, timedelta

daylinks=[
  "https://web.archive.org/web/20230921171818/dailycaller.com/section/politics",
  "https://web.archive.org/web/20230915031132/dailycaller.com/section/politics",
  "https://web.archive.org/web/20230909222026/dailycaller.com/section/politics"
]

totallinks=[]
print("Gathering Links...")
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
  # for l in links:
  #   print(l)
  politicnews = links
  politicnews = [link for link in politicnews if link is not None]
  #print(politicnews)
  politicnews = [link for link in politicnews if '/2023/09/' in link]
  politicnews = [link[20:] for link in politicnews]
  for link in politicnews:
    if link.startswith("https"):
      #print(link)
      totallinks.append(link)
  time.sleep(2)


print("Gathering texts...")
totallinks = list(set(totallinks))
print(len(totallinks))
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
  # if(len(paragraphs)<1):
  #   print(soup)
  #   print("END OF SOUP")
  text = ""
  for p in paragraphs:
    if p.get_text()==paragraphs[0].get_text():
      continue
    text = text + " " + p.get_text()
    text = text.replace('Advertisement','')
    text = text.replace('DAILY CALLER','')
    text = text.replace('Daily Caller','')
    text = text.replace('The Daily Caller','')
  try:
    index = text.find("All content created by the  News Foundation")
    if index!=-1:
      text = text[:index]
  except:
    print("nothere")
  try:
    index = text.find("TRENDING ©2024")
    if index!=-1:
      text = text[:index]
  except:
    print("nothere")
  texts.append(text)
  #print(text)
  time.sleep(1.5)

print(len(texts))

with open('dataset/dc.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)