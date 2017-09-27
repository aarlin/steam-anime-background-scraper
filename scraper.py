# BeautifulSoup implementation

import re
import json
from urllib import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver



def pagescraper(searchpage):
    ''' Takes a steam store search url and 
    scrapes all the game store page url '''

    steamApps = set()

    html = urlopen(searchpage)
    bsObj = BeautifulSoup(html.read())
    for link in bsObj.findAll("a", href = re.compile("^(http://store.steampowered.com/app/.*)$")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in steamApps:
                newApp = link.attrs['href'].split('/')[4]
                print("New steam app added to list: " + newApp)
                steamApps.add(newApp)

    return steamApps

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

def pagefindermarketscraper(searchpage):
    
    driver = webdriver.PhantomJS()
    driver.get(searchpage)

    html = driver.page_source
    bsObj = BeautifulSoup(html)

    span = bsObj.find("span", id = "searchResults_links")
    page = 1
    try:
        page = span.findAll("span")[-1].text
    except IndexError:
        pass
    except AttributeError:
        pass

    return page
         
def imagescraper(searchpage):
    ''' Takes a background community item page and returns the large size and full size image '''

    driver = webdriver.PhantomJS()
    driver.get(searchpage)

    html = driver.page_source
    bsObj = BeautifulSoup(html)
    
    # not loaded on initial html.read(), rather it is done by javascript

    largeimage = [div.img['src'] for div in bsObj.findAll("div", {"class" : "market_listing_largeimage"}) if div.img]
    fullsizeimage = [div.a['href'] for div in bsObj.findAll("div", {"class" : "item_actions"}) if div.a]

    return largeimage, fullsizeimage

def marketitemscraper(searchpage):
    ''' Takes a steam app id and scrapes the community market page for all related items shown on page'''
    html = urlopen(searchpage)         
    bsObj = BeautifulSoup(html.read())

    if bsObj.find("div", {"class" : "error_ctn"}):
        print("You've made too many requests recently. Please wait and try your request again later.")
        quit()

    data = {}
    data['background'] = []
    data['trading_card'] = []
    data['emoticon'] = []

    for link in bsObj.findAll("a", {"class": "market_listing_row_link"}):
        price = link.findAll("span", {"class": "normal_price"})[-1].text
        itemname = link.find("span", {"class": "market_listing_item_name"}).text
        itemtype = link.find("span", {"class": "market_listing_game_name"}).text

        if 'Trading Card' in itemtype:
            # FOR FUTURE USE
            pass
        elif 'Emoticon' in itemtype:
            # FOR FUTURE USE
            pass
        elif 'Booster Pack' in itemtype:
            # FOR FUTURE USE
            pass
        elif 'Profile Background' in itemtype:
            largeimage, fullsizeimage = imagescraper(link['href'])     

            background_data = {}
            background_data['name'] = itemname
            background_data['price'] = price
            background_data['type'] = itemtype
            background_data['largeimg'] = largeimage[0]
            background_data['fullsizeimg'] = fullsizeimage[0]
            background_data['market_hash_name'] = link['href'].split('/')[-1].split('?filter=')[0]

            data['background'].update(background_data)

        else:
            print("There was an error with this item type: " + itemtype)

    return data

# def fullmarketitemscraper(searchpage):
#     ''' Grabs all items from a specific steam app id from all pages of steam app's market '''
#     totalpages = pagefindermarketscraper(searchpage)

#     data = {}

#     for page in range(1, int(totalpages) + 1):
#         if page == 1:
#             marketdata = marketitemscraper(searchpage)
#             data['background'].append(marketdata['background'])
#             print("Finished scraping page 1")
#         else:
#             separator = "#p"
#             marketpage = searchpage.split(separator, 1)[0]
#             marketpage += "#p" + str(page) + "_popular_desc"

#             marketdata = marketitemscraper(marketpage)
#             data['background'].append(marketdata['background'])
#             print("Finished scraping page " + str(page))

def backgroundscraper(steamapp):
    marketpage = "http://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_" + str(steamapp) + "&q=background"
    totalpages = pagefindermarketscraper(marketpage)
    data = {}
    data['background'] = []

    for page in range(1, int(totalpages) + 1):
        if page == 1:
            marketdata = marketitemscraper(marketpage)
            data['background'].append(marketdata['background'])
            print("Finished scraping page 1 of backgrounds")
        else:
            separator = "#p"
            marketpage = marketpage.split(separator, 1)[0]
            marketpage += "#p" + str(page) + "_popular_desc"

            marketdata = marketitemscraper(marketpage)
            data['background'].append(marketdata['background'])
            print("Finished scraping page " + str(page) + " of backgrounds")

    return data

def tradingcardscraper(steamapp):
    marketpage = "http://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_" + str(steamapp) + "&q=trading+card"
    totalpages = pagefindermarketscraper(marketpage)
    data = {}
    data['trading_card'] = []   

    for page in range(1, int(totalpages) + 1):
        if page == 1:
            marketdata = marketitemscraper(marketpage)
            data['trading_card'].append(marketdata['trading_card'])
            print("Finished scraping page 1 of trading cards")
        else:
            separator = "#p"
            marketpage = marketpage.split(separator, 1)[0]
            marketpage += "#p" + str(page) + "_popular_desc"

            marketdata = marketitemscraper(marketpage)
            data['trading_card'].append(marketdata['trading_card'])
            print("Finished scraping page " + str(page) + " of trading cards") 

    return data

def emoticonscraper(steamapp):
    marketpage = "http://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_" + str(steamapp) + "&q=emoticon"
    totalpages = pagefindermarketscraper(marketpage)
    data = {}
    data['emoticon'] = []  

    for page in range(1, int(totalpages) + 1):
        if page == 1:
            marketdata = marketitemscraper(marketpage)
            data['emoticon'].append(marketdata['emoticon'])
            print("Finished scraping page 1 of emoticons")
        else:
            separator = "#p"
            marketpage = marketpage.split(separator, 1)[0]
            marketpage += "#p" + str(page) + "_popular_desc"

            marketdata = marketitemscraper(marketpage)
            data['emoticon'].append(marketdata['emoticon'])
            print("Finished scraping page " + str(page) + " of emoticons")   

    return data

def marketscraper(appid):
    print("Running scraper on steam app id: " + str(appid))
    appids = {}
    appids[appid] = {}
    backgrounds = backgroundscraper(appid)
    tradingcards = tradingcardscraper(appid)
    emoticons = emoticonscraper(appid)
    appids[appid].update(backgrounds)
    appids[appid].update(tradingcards)
    appids[appid].update(emoticons)

    with open('animegames.json', 'a') as output:
        json.dump(appids, output)

def allgamemarketscraper(appids):
    print ("OK")

def animeBackgroundsScraper():
    ''' Rather than use steam store for their tag for anime games, 
    Anime Backgrounds steam group already has one compiled since 2014 '''

    appids = {}

    html = urlopen('https://animebackgrounds.co/database/')
    bsObj = BeautifulSoup(html.read())

    for anchor in bsObj.findAll("a", href = re.compile("^(http://www.steamcardexchange.net/.*)$")):
        if 'href' in anchor.attrs:
            appid = (anchor.attrs['href']).split('-appid-')[-1] # GRAB THE APPID
            if appid not in appids:
                appids[appid] = anchor.text # PLACEHOLDER, WILL BE FIXED

    # GRAB THE NAME OF THE APP ID FROM STEAM API
    # GRABBING FROM THIS SITE IS UNRELIABLE BECAUSE OF ENCODING ISSUES

    for keys in appids:
        url = "http://store.steampowered.com/apidetails/?appids=" + appid
        response = urlopen(url)
        responseJson = json.loads(response.read())
        print responseJson.get("data")
        


    for key, value in appids.items():
        print("Key", key, 'points to', value)

    print len(appids.keys())


# EXAMPLE FUNCTION USAGE

#pagescraper("http://store.steampowered.com/search/?tags=4085&category2=29")
#totalpages("http://store.steampowered.com/search/?tags=4085&category2=29")
#allpagescraper("http://store.steampowered.com/search/?tags=4085&category2=29")
#marketitemscraper("http://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_415480")
#pagefindermarketscraper("http://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_415480")
#pagefindermarketscraper("http://steamcommunity.com/market/search?")
#marketscraper(415480)
animeBackgroundsScraper()

# SO WE HAVE SCRAPER FOR ALL ANIME GAMES
# THAT GIVES US STEAM APP ID FOR THOSE GAMES
# WE USE THOSE APP ID TO OBTAIN BACKGROUND IMG.

# NEED TO WORK ON ADDING EXCEPTIONS TO APP ID
# NEED TO WORK ON CONVERTING DATA INTO READABLE FORMAT, JSON
# RARITY OF ITEM TYPE? UNCOMMON, RARE, COMMON?
# FIX UP DEFINITIONS


# MAKE SEPARATE FUNCTIONS FOR BACKGROUND, CARD, EMOTICONS??
# TRYING TO GRAB EVERYTHING AT ONCE IS TROUBLESOME ATM 