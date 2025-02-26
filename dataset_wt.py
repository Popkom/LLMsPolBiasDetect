import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
from datetime import datetime, timedelta

daylinks=[
  "https://web.archive.org/web/20230930184055/washingtontimes.com/news/politics",
  "https://web.archive.org/web/20230929180153/washingtontimes.com/news/politics",
  "https://web.archive.org/web/20230928173714/washingtontimes.com/news/politics",
  "https://web.archive.org/web/20230927151846/washingtontimes.com/news/politics",
  "https://web.archive.org/web/20230926143904/washingtontimes.com/news/politics",
  "https://web.archive.org/web/20230925140611/washingtontimes.com/news/politics",
  "https://web.archive.org/web/20230924132127/washingtontimes.com/news/politics"
]

# print("Getting Wayback Snapshots...")
# base_url = "http://web.archive.org/cdx/search/cdx"
# url = "https://washingtontimes.com/news/politics"
# daylinks = []
# start_date = datetime(2023,9,20)
# end_date = datetime(2023,9,30)
# delta = timedelta(days=1)

# curr_date = start_date
# while curr_date<=end_date:
#   print(curr_date)
#   day_start = curr_date.strftime("%Y%m%d")
#   day_end = (curr_date+delta).strftime("%Y%m%d")
#   params = {
#     "url": url,
#     "output": "json",
#     "from": day_start,
#     "to": day_end,
#     "filter": "statuscode:200",
#   }
  
#   response = requests.get(base_url, params=params)
#   time.sleep(1.5)
#   if response.status_code == 200:
#     data = response.json()
#     if len(data) > 1:
#       latest_snapshot = data[-1]
#       timestamp = latest_snapshot[1]
#       archive_url = f"https://web.archive.org/web/{timestamp}/{url}"
#       daylinks.append(archive_url)
#       with open("dataset/links.json","w") as f:
#         json.dump(daylinks,f,indent=4)
    
#   curr_date += delta
# print("Done")

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
  politicnews = [link for link in politicnews if '/news/2023/sep/' in link]
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
    text = text + " " + p.get_text()
    text = text.replace('Advertisement','')
    text = text.replace('The Washington Times','')
    text = text.replace('THE WASHINGTON TIMES','')
    text = text.replace('Click\n                        ','')
    text = text.replace('\n                        ','')
    text = text.replace('\n','')
    text = text.replace('SEE ALSO:','')
    text = text.replace('WASHINGTON', '')
  try:
    index = text.find("•")
    if index!=-1:
      text = text[:index]
  except:
    print("nothere")
  try:
    index = text.find("Copyright © 2024")
    if index!=-1:
      text = text[:index]
  except:
    print("nothere")
  texts.append(text)
  #print(text)
  time.sleep(1.5)

print(len(texts))

with open('dataset/wt.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)