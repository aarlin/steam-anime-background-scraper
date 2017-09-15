# BeautifulSoup implementation

from urllib import urlopen
from bs4 import BeautifulSoup
import re

steamApps = set()
def pagescraper(searchpage):
    html = urlopen(searchpage)
    bsObj = BeautifulSoup(html.read())
    for link in bsObj.findAll("a", href = re.compile("^(http://store.steampowered.com/app/.*)$")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in steamApps:
                newApp = link.attrs['href']
                print("New steam app added to list: " + newApp)
                steamApps.add(newApp)

def totalpages(searchpage):
    html = urlopen(searchpage)
    bsObj = BeautifulSoup(html.read())
    div = bsObj.find("div", {"class":"search_pagination_right"})
    print(div)


# <a href="http://store.steampowered.com/appa/ + ^*?  + "

# need to go through all pages as well

#pagescraper("http://store.steampowered.com/search/?tags=4085&category2=29")
totalpages("http://store.steampowered.com/search/?tags=4085&category2=29")

#<div class="search_pagination_right">
