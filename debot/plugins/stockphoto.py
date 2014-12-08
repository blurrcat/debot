#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import shuffle
import requests
from bs4 import BeautifulSoup


def on_stockphoto(query):
    """
    `query` - return a shutterstock photo for `query`
    :param query: stock name
    :return: a stock photo
    """
    url = "http://www.shutterstock.com/cat.mhtml?searchterm={}&search_group=&lang=en&language=en&search_source=search_form&version=llv1".format(query)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    images = [x["src"] for x in soup.select(".gc_clip img")]
    shuffle(images)

    return images[0] if images else ""
