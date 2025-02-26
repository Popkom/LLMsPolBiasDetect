import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
from datetime import datetime, timedelta

print("Getting Wayback Snapshots...")
base_url = "http://web.archive.org/cdx/search/cdx"
url = "https://www.slate.com/news-and-politics/politics"
daylinks = []
start_date = datetime(2024,8,31)
end_date = datetime(2024,9,18)
delta = timedelta(days=1)

curr_date = start_date
while curr_date<=end_date:
  print(curr_date)
  day_start = curr_date.strftime("%Y%m%d")
  day_end = (curr_date+delta).strftime("%Y%m%d")
  params = {
    "url": url,
    "output": "json",
    "from": day_start,
    "to": day_end,
    "filter": "statuscode:200",
  }
  
  response = requests.get(base_url, params=params)
  time.sleep(1.5)
  if response.status_code == 200:
    data = response.json()
    if len(data) > 1:
      latest_snapshot = data[-1]
      timestamp = latest_snapshot[1]
      archive_url = f"https://web.archive.org/web/{timestamp}/{url}"
      daylinks.append(archive_url)
      with open("dataset/links.json","w") as f:
        json.dump(daylinks,f,indent=4)
    
  curr_date += delta
print("Done")