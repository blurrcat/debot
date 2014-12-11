#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from debot.plugin_utils import admin_required


@admin_required
def on_reload_plugins(branch='master'):
    """
    `[branch]` - reload plugins in debot
    """
    resp = []
    try:
        git_plugins_manager = current_app.extensions['git_plugins_manager']
    except KeyError:
        pass
    else:
        resp.append(git_plugins_manager.reload(branch))
    dispatcher = current_app.extensions['dispatcher']
    dispatcher.load_hooks()
    resp.append('reloaded all plugins')
    return '\n'.join(resp)
