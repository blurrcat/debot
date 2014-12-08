#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib import quote
import requests


def calc(eq):
    """
    `equation` - return the google calculator result
    """
    query = quote(eq)
    url = "https://encrypted.google.com/search?hl=en&q={}".format(query)
    soup = BeautifulSoup(requests.get(url).text)

    answer = soup.findAll("h2", attrs={"class": "r"})
    if not answer:
        answer = soup.findAll("span", attrs={"class": "_m3b"})
        if not answer:
            return ":crying_cat_face: Sorry, google doesn't have an answer for you :crying_cat_face:"

    # They seem to use u\xa0 (non-breaking space) in place of a comma
    answer = answer[0].text.replace(u"\xa0", ",")
    return answer
