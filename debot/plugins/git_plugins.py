#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from debot.plugin_utils import admin_required


@admin_required
def on_reload_plugins(branch):
    """
    `[branch]` - reload plugins in debot
    """
    git_plugins_manager = current_app.extensions['git_plugins_manager']
    resp = git_plugins_manager.reload(branch)
    dispatcher = current_app.extensions['dispatcher']
    dispatcher.load_hooks()
    return '%s\nreloaded all plugins' % resp
