from pathlib import Path
from bs4 import BeautifulSoup
from os.path import exists
import requests
import hashlib
import re

drawContentsBlocks = []
draws = {}
drawsText = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

with open("eoi.html", encoding="utf-8") as fp:
  data = fp.read()

# r = requests.get("https://immigratemanitoba.com/category/mpnp-notices/eoi-draw/", headers=headers)
# data = r.text

soup = BeautifulSoup(data, features="html.parser")

# Get all URLs
nav = soup.find(id='archives')
nav_lis = nav.find_all('li')
urls = []
for li in nav_lis:
  a = li.find('a')
  urls.append(a['href'])

for link in urls:
  # Get all <article class="post">
  htmlFilename = re.sub(r'[^a-zA-Z0-9]+', '-', link)
  htmlFilename = re.sub(r'https-', '', htmlFilename)
  htmlFilename = re.sub(r'-$', '', htmlFilename)
  htmlFile = Path('cache/' + htmlFilename)
  # print("Processing: " + htmlFilename)
  # print("Checking cache: " + htmlFilename)

  # Does cache file exist
  if (exists(htmlFile)):
    # print("-----Cache exists")
    # Open cache File
    data = open(htmlFile, encoding="utf-8")
  else :
    # Open url
    # print("Opening URL: " + link)
    data = requests.get(link, headers=headers)

    # Save to cache
    with open(htmlFile, 'w', encoding="utf-8") as f:
      f.write(data.text)
      # print("-----Cache created")

  # Parse file
  soup = BeautifulSoup(data, features="html.parser")
  entryContents = soup.find_all(class_='entry-content')

  # Find all entry-content with `Draw #` text
  for entry in entryContents:
    h3 = entry.find(string=re.compile("Draw #([0-9]*)"))
    if(h3):
      drawContentsBlocks.append(entry)

for block in drawContentsBlocks:
  h3 = block.find(string=re.compile("Draw #([0-9]*)"))
  drawNum = re.search('Draw #([0-9]*)', h3.text).group(1)
  swo = block.find(string=re.compile("Skilled Workers Overseas", re.IGNORECASE))
  swoTag = swo.find_parent(["h3","h4","p"])
  swoList = swoTag.find_next_sibling('ul')
  lowestLI = swoList.find(string=re.compile("lowest-ranked", re.IGNORECASE)).find_parent("li")
  score = re.search('([0-9].*)', lowestLI.text).group(1)

  drawsText.append(h3.text + ": " + score )

for draw in drawsText:
  print(draw)