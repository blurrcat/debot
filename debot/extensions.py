#!/usr/bin/env python
# -*- coding: utf-8 -*-
from debot.slack_notify import Notifier
from debot.dispatcher import Dispatcher
from debot.git_plugins import GitPluginsManager


notifier = Notifier()
dispatcher = Dispatcher()
git_plugin_manager = GitPluginsManager()
