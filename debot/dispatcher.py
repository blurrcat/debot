#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
import imp
import os
import re
import sys


class HookError(Exception):
    pass


class Dispatcher(object):
    def __init__(self, app=None, plugins_dirs=None):
        self.logger = None
        self.hooks = {}
        self.docs = {}
        self.summaries = {}
        self.help_all = ''
        self.moto = ''
        self.admins = []
        if plugins_dirs:
            self.plugins_dirs = plugins_dirs
        else:
            self.plugins_dirs = []
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.logger = app.logger
        try:
            self.plugins_dirs.append(app.config['EXTRA_PLUGINS_DIR'])
        except KeyError:
            pass
        self.plugins_dirs.append(os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'plugins')))
        self.plugins_dirs.reverse()  # plugins priority: built-in > fs > git
        self.admins = app.config.get('ADMINS')
        self.moto = app.config.get('MOTO')
        app.extensions['dispatcher'] = self
        self.load_hooks()

    def add_hook(self, modname, command, func, hooks=None):
        """
        add a hook to hook registry
        :param modname: module from which the hook is loaded
        :param command: hook name
        :param func: hook function
        :return: the actual registered command
        """
        # add mod name to avoid command name clashes
        hooks = hooks if hooks is not None else self.hooks
        if command in hooks:
            command = '%s_%s' % (modname, command)
        hooks[command] = func
        if func.__doc__:
            doc = func.__doc__.strip('\n ')
            self.summaries[command] = doc.split('\n')[0]
            self.docs[command] = doc
        return command

    def load_hooks(self):
        hooks = {'help': self._on_help}
        for directory in self.plugins_dirs:
            self.load_plugins(hooks, directory)
        self.hooks = hooks
        self._gen_help()

    def load_plugins(self, hooks, plugin_dir, silent=True):
        if not os.path.isdir(plugin_dir):
            if not silent:
                raise RuntimeError(
                    '"%s" is not a directory or does not exist' % plugin_dir)
            else:
                return
        self.logger.info('loading plugins from %s', plugin_dir)
        sys.path.insert(0, plugin_dir)
        for plugin in glob(os.path.join(plugin_dir, '[!_]*.py')):
            self.logger.info("loading plugin: %s", plugin)
            plugin = os.path.basename(plugin)
            modname = plugin[:-3]
            try:
                fp, pathname, desc = imp.find_module(modname, [plugin_dir])
                try:
                    mod = imp.load_module(modname, fp, pathname, desc)
                finally:
                    if fp:
                        fp.close()
                for command in re.findall(r"on_(\w+)", " ".join(dir(mod))):
                    hookfun = getattr(mod, "on_" + command)
                    command = self.add_hook(modname, command, hookfun, hooks)
                    self.logger.info(
                        "attaching %s - %s to %s", plugin, hookfun, command)
            except:
                # load time error
                self.logger.exception(
                    "import failed on module %s, module not loaded", plugin)
                raise
        self.logger.info('pluggings loaded from %s', plugin_dir)

    def _gen_help(self):
        docs = [self.moto] if self.moto else []
        docs.extend('*%s* %s' % (command, doc)
                    for command, doc in self.summaries.iteritems())
        self.help_all = '\n'.join(docs)

    def _on_help(self, which=None):
        if which:
            try:
                return '*%s* %s' % (which, self.docs[which])
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
