'''
title: Webscraping Functions File
authors: Palaash Kolhe & Shaishav Shah
date created: 2020-06-10

Seperate file for more specific web scrapes... They are based off the live_prices.py file
'''

from bs4 import BeautifulSoup
import requests
from datetime import datetime


def webScrapeURL(url):
    agent = {"User-Agent":"Mozilla/5.0"} # specifies what user-agent to search as
    response = requests.get(url, headers = agent) # using requests module to get the content
    entirePage = BeautifulSoup(response.content, 'html.parser') # converts content into html code
    return entirePage

def getLivePrice(page): # Getting the live prices and a time
    #url = 'https://ca.finance.yahoo.com/quote/{0}'.format(ticker) # The url used
    #response = requests.get(url) # Using requests module to get the content
    #yahoo_price_html = BeautifulSoup(response.content,'html.parser') # Converting content into html code
    tag_with_price_and_time = page.find_all(class_ = 'My(6px) Pos(r) smartphone_Mt(6px)')[0] # This is the class I need to search through, obtained through inspect element in chrome
    price = tag_with_price_and_time.find_all('span')[0].text # Price is in the 1st span element, therefore this works
    time = datetime.now().strftime("%M:%S")
    return price,time


def ScrapeTop(page): # returns ticker, last, change, volume
    #website = BeautifulSoup(self.response.content, 'html.parser')
    array = []
    all_stocks = page.find_all('table', class_='t-home-table')[0]
    for line in all_stocks.find_all('tr'):
        stock_info = []
        mini_array = line.find_all('td')
        for i in range(4):
            stock_info.append(mini_array[i].text)
        array.append(stock_info)
    array.pop(0)
    return array

def ScrapeDown(page):
    #website = BeautifulSoup(self.response.content, 'html.parser')
    array = []
    all_stocks = page.find_all('table', class_='t-home-table')[1]
    for line in all_stocks.find_all('tr'):
        stock_info = []
        mini_array = line.find_all('td')
        for i in range(4):
            stock_info.append(mini_array[i].text)
        array.append(stock_info)
    array.pop(0)
    return array

def getNewsStock(page):
    newsArray = [] # [news content, publisher, link]
    for data in page.findAll("div", {"class": "news-link-container"}): # searches for news class in entire page
        newsText = data.findAll(text=True) # returns all text and publisher
        newsLink = data.find('a').get('href') # search for links
        newsArray.append([newsText[0], newsText[1], newsLink]) # append to array to be used to find news sources
    return newsArray

def getStockInfo(page): # returns stock name, full stock name, index, price, change, market cap (IN THAT ORDER)
    stockName = page.find('a', {'id': 'ticker'}).text # find stock name
    title = page.find('title').text # find full name of stock
    title = title.replace(stockName + ' ', '') # removes the ticker from the stockname
    title = title.replace(',', '')

    searchText = ('Index', 'Market Cap', 'Change', 'Dividend %', 'P/E', '52W High', '52W Low', 'Perf Week', 'Perf Month', 'Perf Year', 'Perf YTD')

    info = [title, stockName]

    for i in range(len(searchText)):
        textSearch = page.find(text=searchText[i])
        idTag = textSearch.parent
        info.append(idTag.findNext('td').text)

    return info

if __name__ == '__main__':
    applePage = webScrapeURL("https://finviz.com/quote.ashx?t=AAPL")
    getStockInfo(applePage)



