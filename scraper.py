# BeautifulSoup implementation

import re
from urllib import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver

steamApps = set()
def pagescraper(searchpage):
    ''' Takes a steam store search url and 
    scrapes all the game store page url '''

    html = urlopen(searchpage)
    bsObj = BeautifulSoup(html.read())
    for link in bsObj.findAll("a", href = re.compile("^(http://store.steampowered.com/app/.*)$")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in steamApps:
                newApp = link.attrs['href']
                print("New steam app added to list: " + newApp)
                steamApps.add(newApp)

def pagefinder(searchpage):
    ''' Takes a steam store search page url and 
    returns the number to the last page of the search '''
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
    ''' Uses both pagescraper and pagefinder functions and 
    scrapes all pages for all game store url '''
    totalpages = pagefinder(searchpage)
    for page in range(1, totalpages + 1):
        if page == 1:
            pagescraper(searchpage)
        else:
            modifiedsearchpage = searchpage + "&page=" + str(page)
            pagescraper(modifiedsearchpage)

def backgroundscraper(searchpage):
    ''' Takes a background community item page and returns the large size and full size image '''

    driver = webdriver.PhantomJS()
    driver.get(searchpage)

    html = driver.page_source
    bsObj = BeautifulSoup(html)
    
    # not loaded on initial html.read(), rather it is done by javascript

    largeimage = [div.img['src'] for div in bsObj.findAll("div", {"class" : "market_listing_largeimage"}) if div.img]
    print largeimage

    fullsizeimage = [div.a['href'] for div in bsObj.findAll("div", {"class" : "item_actions"}) if div.a]
    print fullsizeimage

     

def marketitemscraper(steamapp):
    ''' Takes a steam app id and scrapes the community market for all related items'''
    searchpage = "http://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_" + str(steamapp)
    html = urlopen(searchpage)         
    bsObj = BeautifulSoup(html.read())

    for link in bsObj.findAll("a", {"class": "market_listing_row_link"}):
        price = link.find("span", {"class": "normal_price"}).text
        itemname = link.find("span", {"class": "market_listing_item_name"}).text
        itemtype = link.find("span", {"class": "market_listing_game_name"}).text

        if 'Trading Card' in itemtype:
            # FOR FUTURE USE
            print(itemtype)
        elif 'Emoticon' in itemtype:
            # FOR FUTURE USE
            print(itemtype)
        elif 'Booster Pack' in itemtype:
            # FOR FUTURE USE
            print(itemtype)
        elif 'Profile Background' in itemtype:
            print(itemtype)
            backgroundscraper(link['href'])
        else:
            print("There was an error with this item type: " + itemtype)

# EXAMPLE FUNCTION USAGE

#pagescraper("http://store.steampowered.com/search/?tags=4085&category2=29")
#totalpages("http://store.steampowered.com/search/?tags=4085&category2=29")
#allpagescraper("http://store.steampowered.com/search/?tags=4085&category2=29")
marketitemscraper(415480)

