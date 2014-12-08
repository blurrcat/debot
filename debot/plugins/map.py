#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import shlex
from urllib import quote


parser = ArgumentParser()
parser.add_argument('place')
parser.add_argument('-z', '--zoom', type=int)
parser.add_argument('-m', '--maptype', default='roadmap')


def on_map(query):
    """
    `[-z ZOOM] [-m MAPTYPE] place` - return a map of place

    Examples:

        !map singapore
        !map "united states" --zoom 4
        !map "united states" -z 4 -m satellite
    """
    args = parser.parse_args(shlex.split(query))
    query = quote(" ".join(args.place))
    url = "https://maps.googleapis.com/maps/api/staticmap?size=800x400&markers=size:tiny%7Ccolor:0xAAAAAA%7C{}&maptype={}"
    url = url.format(query, args.maptype)
    if args.zoom:
        url += "&zoom={}".format(args.zoom)

    return url
