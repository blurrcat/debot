#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import json
from debot.plugin_utils import require_admin


def test_command(app, slack_token, echo_command):
    with app.test_client() as c:
        what = 'hello'
        resp = c.post('/', data={
            'token': slack_token,
            'user_name': 'blurrcat',
            'text': '!debot echo %s' % what,
            'trigger_word': '!debot'
        })
        assert resp.status_code == 200
        resp = json.loads(resp.data)
        assert resp['text'] == what
        # not enough arguments
        resp = c.post('/', data={
            'token': slack_token,
            'user_name': 'blurrcat',
            'text': '!debot echo',
            'trigger_word': '!debot'
        })
        assert resp.status_code == 200
        assert 'argument' in resp.data
        # get help
        resp = c.post('/', data={
            'token': slack_token,
            'user_name': 'blurrcat',
            'text': '!debot help echo',
            'trigger_word': '!debot'
        })
        assert resp.status_code == 200
        resp = json.loads(resp.data)
        assert echo_command.__doc__ in resp['text']


def test_admin(app, slack_token, echo_command, dispatcher):
    admin = 'admin'
    app.config['ADMINS'] = ('admin',)
    dispatcher.hooks[echo_command.__name__] = require_admin(echo_command)
    what = 'hello'
    # admin can call
    with app.test_client() as c:
        resp = c.post('/', data={
            'token': slack_token,
            'user_name': admin,
            'text': '!debot echo %s' % what,
            'trigger_word': '!debot'
        })
        assert resp.status_code == 200
        assert what in resp.data
        # non-admin cannot
        resp = c.post('/', data={
            'token': slack_token,
            'user_name': admin + 'xxx',
            'text': '!debot echo %s' % what,
            'trigger_word': '!debot'
        })
        assert resp.status_code == 200
        assert what not in resp.data
        assert 'not allowed' in resp.data


def test_invalid_command(app, slack_token):
    with app.test_client() as c:
        resp = c.post('/', data={
            'token': slack_token,
            'user_name': 'blurrcat',
            'text': '!debot invalid_command',
            'trigger_word': '!debot'
        })
        assert resp.status_code == 200
        assert 'No such command' in resp.data
