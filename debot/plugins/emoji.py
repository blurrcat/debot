#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from emojicodedict import emojiCodeDict


def on_emoji(n=1):
    """
    `[n]` - return n random emoji
    """
    try:
        n = int(n)
    except ValueError:
        return "n must be an integer"
    emoji = []
    for i in range(n):
        emoji.append(emojiCodeDict[random.choice(emojiCodeDict.keys())])

    return "".join(emoji)
