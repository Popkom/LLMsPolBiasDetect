import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
from datetime import datetime, timedelta

daylinks=[
    "https://web.archive.org/web/20230901234006/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230902022815/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230903000331/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230904004002/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230905012029/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230906020004/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230907204548/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230908014519/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230909023821/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230910031837/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230911040530/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230912051452/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230913053217/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230914060840/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230915063327/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230916072934/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230917081121/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230918092031/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230919095523/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230920105208/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230921110957/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230922115256/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230923124233/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230924132142/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230925140922/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230926145331/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230927162834/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230928172336/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230929155446/https://usatoday.com/news/politics",
    "https://web.archive.org/web/20230930171115/https://usatoday.com/news/politics"
]

# print("Getting Wayback Snapshots...")
# base_url = "http://web.archive.org/cdx/search/cdx"
# url = "https://usatoday.com/news/politics"
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
  politicnews = [link for link in politicnews if 'story/news/politics/2023/09/' in link]
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
    if "Contributing:" in p.get_text():
      continue
    text = text + " " + p.get_text()
    text = text.replace('Advertisement','')
    text = text.replace('USA Today','')
    text = text.replace('USA TODAY','')
    text = text.replace('Fernando Cervantes Jr. is a trending news reporter for . Reach him at fernando.cervantes@gannett.com and follow him on X @fern_cerv_.', '')
    text = text.replace('Eric Lagatta covers breaking and trending news for . Reach him at elagatta@gannett.com','')
    text = text.replace('Cy Neff reports on Wyoming politics for . You can reach him at cneff@usatoday.com or on X, formerly known as Twitter, @CyNeffNews','')
    text = text.replace('Audrey Gibbs is a music reporter for The Tennessean. You can reach her at agibbs@tennessean.com.','')
    text = text.replace('Michael Collins covers the White House. Follow him on X @mcollinsNEWS.','')
    text = text.replace('Reach Joey Garrison on X, formerly Twitter, @joeygarrison.','')
    text = text.replace('Saman Shafiq is a trending news reporter for . Reach her at sshafiq@gannett.com and follow her on X and Instagram @saman_shafiq7.','')
    text = text.replace('Reach Joey Garrison on X @joeygarrison.','')
    text = text.replace('Michael Collins and Joey Garrison cover the White House. Follow Collins on X @mcollinsNEWS and Garrison @joeygarrison','')
    text = text.replace('Swapna Venugopal Ramaswamy is a White House correspondent for . You can follow her on X, formerly Twitter, @SwapnaVenugopal','')
    text = text.replace('Bryce Buyakie is a reporter for the  Network. He can be reached by email at bbuyakie@gannett.com or on X, formerly known as Twitter, @bryce_buyakie.','')
    text = text.replace('Jessie Balmert is a political reporter for the  Network Ohio Bureau, which serves the Columbus Dispatch, Cincinnati Enquirer, Akron Beacon Journal and 18 other affiliated news organizations across Ohio. She can be reached at jbalmert@gannett.com.','')
    text = text.replace('Contact IndyStar politics Pulliam fellow Nadia Scharf at nscharf@indystar.com or follow her on Twitter @nadiaascharf.','')
    text = text.replace('Rachel Barber is a 2024 election fellow at , focusing on politics and education. Follow her on X, formerly Twitter, as @rachelbarber_','')
    text = text.replace('Contact Paul Egan: 517-372-8660 or pegan@freepress.com. Follow him on X, @paulegan4.','')
    text = text.replace('Reach reporter Hannah Pinski at @hpinski@courier-journal.com or follow her on X, formerly known as Twitter, at @hannahpinski.','')
    text = text.replace('Asher Stockler is a reporter for The Journal News and the  Network New York. You can send him an email at astockler@lohud.com. Reach him securely: asher.stockler@protonmail.com.','')
    text = text.replace('Contact Xerxes Wilson at (302) 324-2787 or xwilson@delawareonline.com.','')
    text = text.replace('Taylor Ardrey is a news reporter for . You can reach her at tardrey@gannett.com.','')
    text = text.replace('Reach reporter Hannah Pinski at @hpinski@courier-journal.com or follow her on X, formerly known as Twitter, at @hannahpinski.','')
    text = text.replace('Michael Collins covers the White House. Follow him on X, formerly Twitter, @mcollinsNEWS.','')

  #print(text)
  if ("episode of The Excerpt podcast:" not in text) and ('On a special episode' not in text):
    texts.append(text)
  time.sleep(1.5)

print(len(texts))

with open('dataset/ust.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)