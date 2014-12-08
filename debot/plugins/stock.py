#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from urllib import quote


def on_stockprice(ticker):
    """
    `ticker` - return price of a stock
    Example: !stockprice $goog
    """
    match = re.findall(r"\$\w{0,4}", ticker)
    if not match:
        return "Nothing found"
    url = "https://www.google.com/finance?q={}"
    soup = BeautifulSoup(requests.get(url.format(quote(ticker))).text)

    company, ticker = re.findall(u"^(.+?)\xa0\xa0(.+?)\xa0", soup.text, re.M)[0]
    price = soup.select("#price-panel .pr span")[0].text
    change, pct = soup.select("#price-panel .nwp span")[0].text.split()
    pct.strip('()')

    emoji = ":chart_with_upwards_trend:" if change.startswith("+") else ":chart_with_downwards_trend:"

    return "{} {} {}: {} {} {} {}".format(emoji, company, ticker, price, change, pct, emoji)
