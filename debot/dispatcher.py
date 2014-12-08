#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
import importlib
import os
import re
import sys


class HookError(Exception):
    pass


class Dispatcher(object):
    def __init__(self, app=None):
        self.logger = None
        self.hooks = {}
        self.docs = {}
        self.summaries = {}
        self.help_all = ''
        self.admins = []
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.logger = app.logger
        plugin_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'plugins'))
        self.hooks['help'] = self._on_help
        self._load_plugins(plugin_dir)
        self._load_plugins(app.config.get('DEBOT_PLUGINS_DIR', ''))
        self.admins = app.config.get('')
        self._gen_help(app.config.get('MOTO', ''))
        app.extensions['dispatcher'] = self

    def _add_hook(self, modname, command, func):
        """
        add a hook to hook registry
        :param modname: module from which the hook is loaded
        :param command: hook name
        :param func: hook function
        :return: the actual registered command
        """
        # add mod name to avoid command name clashes
        if command in self.hooks:
            command = '%s_%s' % (modname, command)
        self.hooks[command] = func
        if func.__doc__:
            self.summaries[command] = func.__doc__.split('\n')[0]
            self.docs[command] = func.__doc__
        return command

    def _load_plugins(self, plugin_dir, silent=True):
        if not os.path.isdir(plugin_dir):
            if not silent:
                raise RuntimeError(
                    '"%s" is not a directory or does not exist' % plugin_dir)
            else:
                return
        sys.path.insert(0, plugin_dir)
        for plugin in glob(os.path.join(plugin_dir, '[!_]*.py')):
            self.logger.info("loading plugin: %s", plugin)
            plugin = os.path.basename(plugin)
            modname = plugin[:-3]
            try:
                mod = importlib.import_module(modname)
                for command in re.findall(r"on_(\w+)", " ".join(dir(mod))):
                    hookfun = getattr(mod, "on_" + command)
                    command = self._add_hook(modname, command, hookfun)
                    self.logger.info(
                        "attaching %s - %s to %s", plugin, hookfun, command)
            except:
                # load time error
                self.logger.exception(
                    "import failed on module %s, module not loaded", plugin)
                raise

    def _gen_help(self, moto=None):
        docs = [moto] if moto else []
        docs.extend('*%s*: %s' % (command, doc)
                    for command, doc in self.summaries.iteritems())
        self.help_all = '\n'.join(docs)

    def _on_help(self, which=None):
        if which:
            try:
                return self.docs[which]
            except KeyError:
                return 'No such command'
        else:
            return self.help_all

    def dispatch(self, command, args=None):
        try:
            hook = self.hooks[command]
        except KeyError:
            return 'No such command: %s' % command
        try:
            if args:
                return hook(args)
            else:
                return hook()
        except Exception as e:
            self.logger.exception('error running command %s', command)
            raise HookError('Error running command %s: %s' % (command, e))
