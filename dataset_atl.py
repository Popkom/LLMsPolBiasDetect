import requests
import json
import time
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen

daylinks=["https://web.archive.org/web/20230930214155/theatlantic.com/politics",
          "https://web.archive.org/web/20230928201436/theatlantic.com/politics",
          "https://web.archive.org/web/20230925210510/theatlantic.com/politics",
          "https://web.archive.org/web/20230923210155/theatlantic.com/politics",
          "https://web.archive.org/web/20230921134825/theatlantic.com/politics",
          "https://web.archive.org/web/20230919073754/theatlantic.com/politics",
          "https://web.archive.org/web/20230916193311/theatlantic.com/politics",
          "https://web.archive.org/web/20230914132728/theatlantic.com/politics",
          "https://web.archive.org/web/20230913000716/theatlantic.com/politics",
          "https://web.archive.org/web/20230910134229/theatlantic.com/politics",
          "https://web.archive.org/web/20230908123836/theatlantic.com/politics",
          "https://web.archive.org/web/20230906164243/theatlantic.com/politics",
          "https://web.archive.org/web/20230904052223/theatlantic.com/politics",
          "https://web.archive.org/web/20230902153305/theatlantic.com/politics",
          "https://web.archive.org/web/20230918035128/theatlantic.com/politics"]
totallinks=[]
for link in daylinks:
  req = Request(
      url=link, 
      headers={'User-Agent': 'Mozilla/5.0'}
  )
  page = urlopen(req).read()
  soup = BeautifulSoup(page, 'html.parser')
  atags = soup.find_all('a')
  links = [atag.get('href') for atag in atags]
  # for l in links:
  #   print(l)
  politicnews = links
  politicnews = [link[43:] for link in politicnews]
  politicnews = [link for link in politicnews if 'politics/archive/2023/' in link]
  for link in politicnews:
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
    text = text.replace('Advertisement','')
    text = text.replace('The Atlantic','')
    text = text.replace(' Produced by ElevenLabs and News Over Audio (NOA) using AI narration.', '')
  
  try:
    index = text.find("More Stories")
    if index!=-1:
      text = text[:index]
  except:
    print("nothere")
  #print(text)
  texts.append(text)

print(len(texts))

with open('dataset/atlantic.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)