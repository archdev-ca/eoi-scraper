from pathlib import Path
from bs4 import BeautifulSoup
from os.path import exists
import requests
import hashlib
import re
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

with open("eoi.html", encoding="utf8") as fp:
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
  print("Checking cache: " + htmlFilename)

  # Does cache file exist
  if (exists(htmlFile)):
    # Open cache File
    data = open(htmlFile)
  else :
    # Open url
    print("Opening URL: " + link)
    data = requests.get(link, headers=headers)

    # Save to cache
    with open(htmlFile, 'w', encoding="utf-8") as f:
      f.write(data.text)



    # Loop through each article

  # Check for title <h1 class="entry-title"><a>EOI Draw</a></h1>
