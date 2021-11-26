from bs4 import BeautifulSoup
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

with open("eoi.html", encoding="utf8") as fp:
  data = fp.read()

# r = requests.get("https://immigratemanitoba.com/category/mpnp-notices/eoi-draw/", headers=headers)
# data = r.text

soup = BeautifulSoup(data)

# Get all URLs
nav = soup.find(id='archives')
nav_lis = nav.find_all('li')
urls = []
for li in nav_lis:
  a = li.find('a')
  urls.append(a['href'])

for link in urls:
  print(link)

  # Get all <article class="post">

    # Loop through each article

  # Check for title <h1 class="entry-title"><a>EOI Draw</a></h1>
