# BeautifulSoup implementation

from urllib import urlopen
from bs4 import BeautifulSoup
import re

def pagescraper(searchpage):
    html = urlopen(searchpage)
    bsObj = BeautifulSoup(html.read())
    for link in bsObj.findAll("a", href = re.compile("^(http://store.steampowered.com/app/.*)$")):
        if 'href' in link.attrs:
            print(link.attrs['href'])

def totalpages(searchpage):
    html = urlopen(searchpage)


# <a href="http://store.steampowered.com/appa/ + ^*?  + "

# need to go through all pages as well

pagescraper("http://store.steampowered.com/search/?tags=4085&category2=29")

#<div class="search_pagination_right">
