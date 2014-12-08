#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from urllib import quote
import requests


def on_youtube(query):
    """
    `query` - return the first youtube search result for `query`
    :param query: a list of terms to search
    """
    query = quote(query)
    url = "https://gdata.youtube.com/feeds/api/videos?q={}&orderBy=relevance&alt=json"
    url = url.format(query)
    j = requests.get(url).json()

    results = j["feed"]
    if "entry" not in results:
        return "sorry, no videos found"

    video = results["entry"][0]["link"][0]["href"]
    video = re.sub("&feature=youtube_gdata", "", video)

    return video
