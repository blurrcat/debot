#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Manage extra plugins via git
"""
import os
import sarge


class GitPluginsManager(object):
    basedir = '/tmp'

    def __init__(self, app=None):
        if not sarge.get_both('which git'):
            raise RuntimeError('git not available')
        self._repo = None
        self._name = None
        self._plugins_dir = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self._repo = app.config['EXTRA_PLUGINS_GIT']
        self._name = self._repo.strip('.git').split('/')[-1]
        self._plugins_dir = os.path.join(
            self.basedir, self._name,
            app.config.get('EXTRA_PLUGINS_GIT_DIR', ''))
        app.extensions['git_plugins_manager'] = self
        self.reload()

    def reload(self, branch='master'):
        """
        get or update plugins from git
        """
        old_cwd = os.getcwd()
        os.chdir(self.basedir)
        try:
            # clone for the first time
            if not os.path.exists(self._name):
                sarge.run('git clone %s' % self._repo)
            os.chdir(self._name)
            codes = sarge.run(
                'git fetch origin && git checkout %s && git pull' % branch
            ).returncodes
            if os.path.exists('requirements.txt'):
                codes.append(
                    sarge.run('pip install -r requirements.txt').returncode)
            for c in codes:
                if c != 0:
                    return 'sth went wrong when pulling plugins from %s' % (
                        self._repo)
            return 'git plugins pulled from %s@%s: "%s"' % (
                self._repo,
                sarge.get_stdout('git rev-parse HEAD').strip('\n')[:8],
                sarge.get_stdout('git log -1 --pretty=%B').strip('\n')
            )
        finally:
            os.chdir(old_cwd)

    @property
    def plugins_dir(self):
        return self._plugins_dir

    @property
    def name(self):
        return self._name
