#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


def on_flip(lst=None):
    """
    `list` - flip a coin n times or shuffle a comma separated list
    Examples:

        !flip
        !flip a, b, c
    """
    lst = lst.split(',') if lst else ['heads', 'tails']
    random.shuffle(lst)
    return ", ".join(i.strip() for i in lst)
