import requests
import json
import time
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen

daylinks = ["https://web.archive.org/web/20230930062830/nypost.com/news",
            "https://web.archive.org/web/20230928234325/nypost.com/news",
            "https://web.archive.org/web/20230926221141/nypost.com/news",
            "https://web.archive.org/web/20230924201458/nypost.com/news",
            "https://web.archive.org/web/20230922150734/nypost.com/news",
            "https://web.archive.org/web/20230920230535/nypost.com/news",
            "https://web.archive.org/web/20230918221453/nypost.com/news",
            "https://web.archive.org/web/20230916211756/nypost.com/news",
            "https://web.archive.org/web/20230914222145/nypost.com/news",
            "https://web.archive.org/web/20230912142707/nypost.com/news",
            "https://web.archive.org/web/20230910140254/nypost.com/news",
            "https://web.archive.org/web/20230908114419/nypost.com/news",
            "https://web.archive.org/web/20230906094347/nypost.com/news",
            "https://web.archive.org/web/20230904084454/nypost.com/news",
            "https://web.archive.org/web/20230902073511/nypost.com/news",
            "https://web.archive.org/web/20230923153041/nypost.com/news",
            "https://web.archive.org/web/20230917134743/nypost.com/news",
            "https://web.archive.org/web/20230913151729/nypost.com/news",
            "https://web.archive.org/web/20230905162850/nypost.com/news"]
totallinks = []
for link in daylinks:
  req = Request(
      url=link, 
      headers={'User-Agent': 'Mozilla/5.0'}
  )
  page = urlopen(req).read()
  soup = BeautifulSoup(page, 'html.parser')
  atags = soup.find_all('a')
  links = [atag.get('href') for atag in atags]
  #print(links)
  politicnews = links[::2]
  politicnews = [link[43:] for link in politicnews]
  politicnews = [link for link in politicnews if '/2023/09/' in link]
  for link in politicnews:
    totallinks.append(link)
  time.sleep(3)

totallinks = list(set(totallinks))
#print(totallinks)

i = 0
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
  script = soup.find('script', type='application/ld+json')
  #print(soup)
  keywords = []
  if script:
    data = json.loads(script.string)
    keywords = data.get('keywords', [])
  print(keywords)
  paragraphs = soup.find_all('p')
  text = ""
  for p in paragraphs:
    text = text + " " + p.get_text()
    text = text.replace('Advertisement','')
    text = text.replace('New York Post','')
  terms = ['/politics','joe biden','donald trump','congress','2024 presidential election','us presidents', 'border wall', 'us border crisis', 'supreme court', 'Israel-Hamas war', 'republicans','white house', 'federal government', 'us border', 'senate', 'us house of representatives', 'democrats', '2020 presidential election']
  matches = any(term in keywords for term in terms)
  if matches:
    texts.append(text)

print(len(texts))


with open('dataset/nypost.csv', 'w',encoding='utf-8', newline='') as nyp:
  wr = csv.writer(nyp)
  for text in texts:
    wr.writerow([text])

print("DONE")