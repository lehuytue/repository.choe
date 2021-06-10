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

    listItem = []

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


def search(url):
    headers2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        , 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
        , 'Accept-Language': 'en-US,en;q=0.5'
    }
    req = urllib.request.Request(url, headers=headers2)
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read(), features="html.parser")
    items = soup.find_all('article')
    # pageNext = soup.find('a', {'class': 'page larger'})

    # strNext = ""
    # if pageNext is not None:
    # strNext = pageNext['href']

    listItem = []

    for item in items:
        src = item.select('div.image div a img')[0].get("src")
        name = item.select('div.details div.title a')[0].get_text()
        href = item.select('div.details div.title a')[0].get("href")
        year = item.select('div.details div.meta span.year')[0].get_text().strip()

        listItem.append({
            'src': src,
            'name': name,
            'href': href,
            'year': year
        })

    return listItem


def getDetail(url):
    headers2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        , 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
        , 'Accept-Language': 'en-US,en;q=0.5'
    }
    req = urllib.request.Request(url, headers=headers2)
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read(), features="html.parser")
    # items = soup.find_all('article')
    sp = soup.find('span', {'class': 'box__download'})
    dllink = sp.select('a')[0]['href']

    req = urllib.request.Request(dllink, headers=headers2)
    f = urllib.request.urlopen(req)
    soup = BeautifulSoup(f.read(), features="html.parser")

    tbl = soup.find('tbody', {'class': 'tbody outer'})

    listItem = []
    for row in tbl.find_all('tr'):
        columns = row.find_all('td')

        src = ''
        name = row.find_all('td')[0].get_text()
        href = row.find_all('td')[1].select('a')[0].get("href")
        year = ''

        listItem.append({
            'src': src,
            'name': name,
            'href': href,
            'year': year
        })

    return listItem


if __name__ == "__main__":
    # listItem = getAll('https://thuvienhd.com/trending')
    # print('listItem:', listItem)

    # listItem = search('https://thuvienhd.com/?s=ch%C3%AD+kh%C3%AD')
    # print('Search:', listItem)

    listItem = getDetail('https://thuvienhd.com/phim/chi-khi-bay-cao-new-horizon-2021')
    print('link:', listItem)
