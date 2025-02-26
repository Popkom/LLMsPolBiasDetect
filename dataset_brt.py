import requests
import json
import time
import http
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen
daylinks=["https://web.archive.org/web/20230930205157/breitbart.com/politics",
          "https://web.archive.org/web/20230928144404/breitbart.com/politics",
          "https://web.archive.org/web/20230926150234/breitbart.com/politics",
          "https://web.archive.org/web/20230924224819/breitbart.com/politics",
          "https://web.archive.org/web/20230922202347/breitbart.com/politics",
          "https://web.archive.org/web/20230920172615/breitbart.com/politics",
          "https://web.archive.org/web/20230918205710/breitbart.com/politics",
          "https://web.archive.org/web/20230916211132/breitbart.com/politics",
          "https://web.archive.org/web/20230914203339/breitbart.com/politics",
          "https://web.archive.org/web/20230912201014/breitbart.com/politics",
          "https://web.archive.org/web/20230910233020/breitbart.com/politics",
          "https://web.archive.org/web/20230908151732/breitbart.com/politics",
          "https://web.archive.org/web/20230906234448/breitbart.com/politics",
          "https://web.archive.org/web/20230904214244/breitbart.com/politics"
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
  # for l in links:
  #   print(l)
  politicnews = links
  politicnews = [link for link in politicnews if link is not None]
  politicnews = [link for link in politicnews if 'politics/2023/09/' in link]
  politicnews = [link[20:] for link in politicnews]
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
    text = text.replace('Advertisement','')
    text = text.replace('Breitbart','')
    text = text.replace("Please let us know if you're having issues with commenting.        \n\n\n\n\n\n\n Copyright © 2024", '')
    text = text.replace("Wendell Husebo is a political reporter with  News and a former RNC War Room Analyst. He is the author of Politics of Slave Morality. Follow Wendell on “X” @WendellHusebø or on Truth Social @WendellHusebo", "")
    text = text.replace("Bradley Jaye is a Capitol Hill Correspondent for  News. Follow him on X/Twitter at @BradleyAJaye", "")
    text = text.replace("Sean Moran is a policy reporter for  News. Follow him on X @SeanMoran3","")
    text = text.replace("Follow  News’s Kristina Wong on ”X”, Truth Social, or on Facebook","")
    text = text.replace("Follow  News’s Kristina Wong on “X”, Truth Social, or on Facebook","")
    text = text.replace("John Binder is a reporter for  News. Email him at jbinder@breitbart.com. Follow him on Twitter here","")
    text = text.replace("John Binder is a reporter for  News. Email him at jbinder@breitbart.com. Follow him on Twitter here.","")
    text = text.replace("Alana Mastrangelo is a reporter for  News. You can follow her on Facebook and X at @ARmastrangelo, and on Instagram","")
    text = text.replace("Katherine Hamilton is a political reporter for  News. You can follow her on X @thekat_hamilton","")
    text = text.replace("Joshua Klein is a reporter for  News. Email him at jklein@breitbart.com. Follow him on Twitter @JoshuaKlein","")
    text = text.replace("Jerome Hudson is  News Entertainment Editor and author of the book 50 Things They Don’t Want You to Know About Trump. Order your copy today. Follow Jerome Hudson on Twitter and instagram@jeromeehudson","")
    text = text.replace("John Nolte’s first and last novel, Borrowed Time, is winning five-star raves from everyday readers. You can read an excerpt here and an in-depth review here. Also available in hardcover and on Kindle and Audiobook","")
    text = text.replace("Joel B. Pollak is Senior Editor-at-Large at  News and the host of  News Sunday on Sirius XM Patriot on Sunday evenings from 7 p.m. to 10 p.m. ET (4 p.m. to 7 p.m. PT). He is the author of The Agenda: What Trump Should Do in His First 100 Days, available for pre-order on Amazon. He is also the author of The Trumpian Virtues: The Lessons and Legacy of Donald Trump’s Presidency, now available on Audible. He is a winner of the 2018 Robert Novak Journalism Alumni Fellowship. Follow him on Twitter at @joelpollak","")
    text = text.replace('Joel B. Pollak is Senior Editor-at-Large at  News and the host of  News Sunday on Sirius XM Patriot on Sunday evenings from 7 p.m. to 10 p.m. ET (4 p.m. to 7 p.m. PT). He is the author of “”The Agenda: What Trump Should Do in His First 100 Days,” available for pre-order on Amazon. He is also the author of “The Trumpian Virtues: The Lessons and Legacy of Donald Trump’s Presidency,” now available on Audible. He is a winner of the 2018 Robert Novak Journalism Alumni Fellowship. Follow him on Twitter at @joelpollak',"")
    text = text.replace("Paul Roland Bois directed the award-winning Christian tech thriller, EXEMPLUM, which has a 100% Rotten Tomatoes critic rating and can be viewed for FREE on YouTube or Tubi. “Better than Killers of the Flower Moon,” wrote Mark Judge. “You haven’t seen a story like this before,” wrote Christian Toto. A high-quality, ad-free rental can also be streamed on Google Play, Vimeo on Demand, or YouTube Movies. Follow him on X @prolandfilms or Instagram @prolandfilms","")
    text = text.replace("News Daily airs on SiriusXM Patriot 125 from 6:00 a.m. to 9:00 a.m. Eastern","")
    text = text.replace("You can follow Alana Mastrangelo on Facebook and X at @ARmastrangelo, and on Instagram.","")
    text = text.replace("You can follow Alana Mastrangelo on Facebook and X at @ARmastrangelo, and on Instagram","")
    text = text.replace("Sean Moran is a policy reporter for  News. Follow him on Twitter @SeanMoran3.","")
    text = text.replace("Sean Moran is a policy reporter for  News. Follow him on Twitter @SeanMoran3","")
    text = text.replace("Emma-Jo Morris is the Politics Editor at  News. Email her at ejmorris@breitbart.com or follow her on Twitter","")
    text = text.replace("News senior legal contributor Ken Klukowski is a lawyer who served in the White House and Justice Department. Follow him on X (formerly Twitter) @kenklukowski","")
    text = text.replace("Wendell Husebo is a political reporter with  News and a former GOP War Room Analyst. He is the author of Politics of Slave Morality. Follow Wendell on “X” @WendellHusebø or on Truth Social @WendellHusebo","")
    text = text.replace("Joel B. Pollak is Senior Editor-at-Large at  News and the host of  News Sunday on Sirius XM Patriot on Sunday evenings from 7 p.m. to 10 p.m. ET (4 p.m. to 7 p.m. PT). He is the author of the recent e-book, “The Trumpian Virtues: The Lessons and Legacy of Donald Trump’s Presidency,” now available on Audible. He is also the author of the e-book, Neither Free nor Fair: The 2020 U.S. Presidential Election. He is a winner of the 2018 Robert Novak Journalism Alumni Fellowship. Follow him on Twitter at @joelpollak","")
  #print(text)
  texts.append(text)
  time.sleep(1.5)

print(len(texts))

with open('dataset/breitbart.json', 'w', encoding='utf8') as json_file:
    json.dump(texts, json_file, ensure_ascii=False)