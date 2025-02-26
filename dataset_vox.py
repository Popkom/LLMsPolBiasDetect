import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
from datetime import datetime, timedelta

daylinks=[
  "https://web.archive.org/web/20230929164017/vox.com/politics",
  "https://web.archive.org/web/20230926004136/vox.com/politics",
  "https://web.archive.org/web/20230921004938/vox.com/politics",
  "https://web.archive.org/web/20230919085429/vox.com/politics",
  "https://web.archive.org/web/20230914161133/vox.com/politics",
  "https://web.archive.org/web/20230912151245/vox.com/politics",
  "https://web.archive.org/web/20230908220912/vox.com/politics",
  "https://web.archive.org/web/20230905192002/vox.com/politics",
  "https://web.archive.org/web/20230902023827/vox.com/politics"
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
  politicnews = [link for link in politicnews if ('/politics/' or '/policy/') in link]
  politicnews = [link[43:] for link in politicnews]
  for link in politicnews:
    if link.startswith("http"):
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
    text = text + " " + p.get_text()
    text = text.replace('Advertisement','')
    text = text.replace('Vox','')
    text = text.replace('VOX','')
    text = text.replace('If you believe in the work we do at , please support us by becoming a member. Our mission has never been more urgent. But our work isn’t easy. It requires resources, dedication, and independence. And that’s where you come in. We rely on readers like you to fund our journalism. Will you support our work and become a  Member today?','')
  try:
    index = text.find("You’ve read")
    if index!=-1:
      text = text[:index]
  except:
    print("nothere")
  texts.append(text)
  #print(text)
  time.sleep(1.5)

print(len(texts))

with open('dataset/vox.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)