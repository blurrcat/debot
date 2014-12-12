#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import sleep
import pytest
from mock import Mock
from debot.slack_notify import Notifier


@pytest.fixture
def notifier(request, app):
    app.config['SLACK_INCOMING_WEBHOOK'] = 'localhost'
    instance = Notifier()
    instance._send = Mock()
    return instance


def test_notify(app, notifier):
    app.config['SLACK_RATE_LIMIT'] = 100
    notifier.init_app(app)
    notifier.notify('1')
    assert not notifier._send.called
    sleep(0.1)
    assert notifier._send.called


def test_notify_now(app, notifier):
    app.config['SLACK_RATE_LIMIT'] = 0.1
    notifier.init_app(app)
    notifier.notify('1', now=True)
    assert notifier._send.called


def test_notify_batch(app, notifier):
    interval = 0.01
    app.config['SLACK_RATE_LIMIT'] = 1 / interval
    notifier.init_app(app)
    notifier.notify('first')
    sleep(1.1 * interval)
    notifier._send.reset_mock()
    # ensured last sent timer
    for i in range(10):
        notifier.notify(unicode(i))
    assert not notifier._send.called
    sleep(1.1 * interval)
    # all messages are combined into 1
    assert notifier._send.call_count == 1
