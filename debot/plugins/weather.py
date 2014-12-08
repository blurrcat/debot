#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time

# http://openweathermap.org/weather-conditions
iconmap = {
    "01": ":sunny:",
    "02": ":partly_sunny:",
    "03": ":partly_sunny:",
    "04": ":cloud:",
    "09": ":droplet:",
    "10": ":droplet:",
    "11": ":zap:",
    "13": ":snowflake:",
    "50": ":umbrella:", #mist?
}


def on_weather(query):
    """
    `query` - return the 5-day forecast for `query`
    :param query: the place to do weather forecast
    :return:
    """
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={0}&cnt=5&mode=json&units=imperial'
    url = url.format(query)

    dat = requests.get(url).json()

    msg = ["{0}: ".format(dat["city"]["name"])]
    for day in dat["list"]:
        name = time.strftime("%a", time.gmtime(day["dt"]))
        high = str(int(round(float(day["temp"]["max"]))))
        icon = iconmap.get(day["weather"][0]["icon"][:2], ":question:")
        msg.append(u"{0} {1}° {2}".format(name, high, icon))

    return " ".join(msg)
