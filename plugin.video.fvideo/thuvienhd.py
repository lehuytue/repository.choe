# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:09:29 2021

@author: congtm
"""
# REQUIRE LIBRARIES
# BeautifulSoup==4.9.3: pip install beautifulsoup4==4.9.3

import urllib.request
from bs4 import BeautifulSoup


def getAll(url):
    headers2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        , 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
        , 'Accept-Language': 'en-US,en;q=0.5'
    }
    req = urllib.request.Request(url, headers=headers2)
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read(), features="html.parser")
    items = soup.find_all('article', class_='item movies')
    # pageNext = soup.find('a', {'class': 'page larger'})

    # strNext = ""
    # if pageNext is not None:
    # strNext = pageNext['href']

    listItem = [];

    for item in items:
        src = item.select('div.poster img')[0].get("src")
        name = item.select('div.data h3 a')[0].get_text()
        href = item.select('div.data h3 a')[0].get("href")
        year = item.select('div.data span')[0].get_text().strip()

        listItem.append({
            'src': src,
            'name': name,
            'href': href,
            'year': year
        })

    return listItem


if __name__ == "__main__":
    listItem = getAll('https://thuvienhd.com/trending')
    print('listItem:', listItem)
