#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import quote
import requests
from bs4 import BeautifulSoup


def on_wiki(query):
    """
    `query` - return the top wiki search result for `query`
    :param query: a list of terms to search
    """
    query = quote(query)

    url = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={0}&format=json"
    url = url.format(query)

    result = requests.get(url).json()

    pages = result["query"]["search"]

    # try to reject disambiguation pages
    pages = [p for p in pages if not 'may refer to' in p["snippet"]]

    if not pages:
        return ""

    page = quote(pages[0]["title"].encode("utf8"))
    link = "http://en.wikipedia.org/wiki/{0}".format(page)

    r = requests.get("http://en.wikipedia.org/w/api.php?format=json&action=parse&page={}".format(page)).json()
    soup = BeautifulSoup(r["parse"]["text"]["*"])
    p = soup.find('p').get_text()
    p = p[:8000]

    return u"{}\n{}".format(p, link)
