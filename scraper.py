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

def pagefinder(searchpage):
    html = urlopen(searchpage)
    bsObj = BeautifulSoup(html.read())
    totalpages = int("0")
    for link in bsObj.find("div", {"class":"search_pagination_right"}).findAll("a"):
        try:
            if int(link.text) > totalpages:
                totalpages = int(link.text)
        except ValueError:  # IGNORE NON-INTEGER VALUES
            continue 
    return totalpages 

def allpagescraper(searchpage):
    totalpages = pagefinder(searchpage)
    for page in range(1, totalpages + 1):
        if page == 1:
            pagescraper(searchpage)
        else:
            modifiedsearchpage = searchpage + "&page=" + str(page)
            pagescraper(modifiedsearchpage)"

def backgroundscraper(searchpage):
    html = urlopen(searchpage)
    bsObj = BeautifulSoup(html.read())

    link = bsObj.find("a", href = re.compile("^(http://cdn.akamai.steamstatic.com/steamcommunity/public/images/items/.*)$"))
    fullsizeimg = link.attrs['href']

    return fullsizeimg

def marketitemscraper(steamapp):
    searchpage = "http://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_" + steamapp
    html = urlopen(searchpage)         
    bsObj = BeautifulSoup(html.read())

    for link in bsObj.findAll("a", href = re.compile("^(https://steamcommunity.com/market/listings/753/.*)$")):
        price = link.find("span", {"class": "normal_price"}).text
        itemname = link.find("span", {"class": "market_listing_item_name"}).text
        itemtype = link.find("span", {"class": "market_listing_game_name"}).text
        if 'Trading Card' in itemtype:
            # FOR FUTURE USE
        elif 'Emoticon' in itemtype:
            # FOR FUTURE USE
        elif 'Profile Background' in itemtype:
            print(backgroundscraper(link.attrs['href']))
        else: 
            print("There was an error with this item type:" + itemtype)

#pagescraper("http://store.steampowered.com/search/?tags=4085&category2=29")
#totalpages("http://store.steampowered.com/search/?tags=4085&category2=29")
allpagescraper("http://store.steampowered.com/search/?tags=4085&category2=29")
