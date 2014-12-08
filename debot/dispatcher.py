#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
from six import importlib
import os
import re


class Dispatcher(object):
    def __init__(self, app=None):
        self.logger = None
        self.hooks = {}
        self.docs = {}
        self.summaries = {}
        self.admins = []
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.logger = app.logger
        plugin_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'plugins'))
        self.hooks['help'] = self.on_help
        self.load_plugins(plugin_dir)
        self.load_plugins(app.config['DEBOT_PLUGINS_DIR'])
        self.admins = app.config.get('')

    def load_plugins(self, plugin_dir, silent=True):
        if not os.path.isdir(plugin_dir):
            if not silent:
                raise RuntimeError(
                    '%s is not a directory or does not exist' % plugin_dir)
            else:
                self.logger.warning(
                    '%s is not a directory or does not exist', plugin_dir)
        for plugin in glob(os.path.join(plugin_dir, '[!_]*.py')):
            self.logger.info("loading plugin: %s", plugin)
            try:
                mod = importlib.import_module(
                    plugin.replace(os.path.sep, ".")[:-3])
                modname = mod.__name__.split('.')[1]
                for command in re.findall("on_(\w+)", " ".join(dir(mod))):
                    hookfun = getattr(mod, "on_" + command)
                    self.logger.info("attaching %s.%s to %s",
                                     modname, hookfun, command)
                    # add mod name to avoid command name clashes
                    if command in self.hooks:
                        command = '%s_%s' % (modname.split('.')[-1], command)
                    self.hooks['!' + command] = hookfun
                    if hookfun.__doc__:
                        self.summaries[command] = mod.__doc__.split('\n')[0]
                        self.docs[command] = mod.__doc__
            except:
                # load time error
                self.logger.exception(
                    "import failed on module %s, module not loaded", plugin)
                raise

    def on_help(self, which=None):
        if which:
            try:
                return self.docs[which]
            except KeyError:
                return 'No such command'
        else:
            return '/n'.join(
                '!%s %s' % (command, doc)
                for command, doc in self.summaries.iteritems())

    def dispatch(self, command, args):
        try:
            hook = self.hooks[command]
        except KeyError:
            return 'No such command: %s' % command
        try:
            return hook(*args)
        except Exception as e:
            self.logger.exception('error running command %s', command)
            return 'Error running command %s: %s' % (command, e)
