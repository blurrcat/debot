#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from flask import current_app, g
from debot.dispatcher import HookError


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not g.user in current_app.config['ADMINS']:
            raise HookError(
                '%s is not allowed to call %s' % (g.user, f.__name__))
        else:
            return f(*args, **kwargs)
    return wrapper

