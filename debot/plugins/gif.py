from argparse import ArgumentParser
import shlex
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import quote
import re
import requests
from random import shuffle


parser = ArgumentParser()
parser.add_argument('query')
parser.add_argument('--unsafe', action='store_true', default=False)


def on_gif(args):
    """
    `query` - return a random result from the google gif search
    """
    args = parser.parse_args(shlex.split(args))
    query = quote(args.query)
    safe = "&safe=" if args.unsafe else "&safe=active"
    searchurl = "https://www.google.com/search?tbs=itp:animated&tbm=isch&q={0}{1}".format(query, safe)

    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Versio  n/4.0.5 Mobile/8A293 Safari/6531.22.7"

    result = requests.get(searchurl, headers={"User-agent": useragent}).text

    gifs = re.findall(r'imgurl.*?(http.*?)\\', result)
    shuffle(gifs)

    return gifs[0] if gifs else ""
