#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from urllib import quote, unquote
import requests


def on_google(q):
    """
    `query`: return the top google result
    :param q:
    :return:
    """
    query = quote(q)
    url = "https://encrypted.google.com/search?q={}".format(query)
    soup = BeautifulSoup(requests.get(url).text)

    answer = soup.findAll("h3", attrs={"class": "r"})
    if not answer:
        return ":crying_cat_face: Sorry, google doesn't have an answer for you :crying_cat_face:"

    return unquote(re.findall(r"q=(.*?)&", str(answer[0]))[0])
