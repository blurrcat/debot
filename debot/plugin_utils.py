#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from flask import current_app, g
from debot.extensions import notifier
from debot.dispatcher import HookError


def admin_required(f):
    """
    Mark a plugin can only be called by admins.
    :param f: plugin function
    :return: decorated plugin function
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not g.user in current_app.config['ADMINS']:
            raise HookError(
                '%s is not allowed to call %s' % (g.user, f.__name__))
        else:
            return f(*args, **kwargs)
    return wrapper


def notify(msg, channel=None, now=False):
    """
    send a message to slack.
    :param msg: message to send
    :param channel: channel to send the message
    :returns: the message if notification is not supported, None otherwise
    """
    notifier.notify(msg, channel, now)


def notify_enabled():
    return 'slack_notifier' in current_app.extensions
