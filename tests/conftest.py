#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest
from debot.app import create_app


@pytest.fixture
def slack_token():
    return 'slack_token'


@pytest.fixture
def app(request, slack_token):
    os.environ['DEBOT_SLACK_TOKEN'] = slack_token
    _app = create_app()
    context = _app.app_context()
    context.push()

    def clean():
        context.pop()

    request.addfinalizer(clean)
    return _app


@pytest.fixture
def dispatcher(app):
    return app.extensions['dispatcher']


@pytest.fixture
def echo_command(app, dispatcher):
    def echo(what):
        """
        echo a string.
        :param what: what to echo
        """
        return what
    dispatcher._add_hook('test_plugins', 'echo', echo)
    dispatcher._gen_help()
    return echo
