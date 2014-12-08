#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import json

"""
Example webhook payload:

    token=wJiUBX2qCcDjdolN5QVyFqjS
    team_id=T0001
    channel_id=C2147483705
    channel_name=test
    timestamp=1355517523.000005
    user_id=U2147483697
    user_name=Steve
    text=googlebot: What is the air-speed velocity of an unladen swallow?
    trigger_word=googlebot:

"""


def test_endpoint(app, slack_token):
    with app.test_client() as c:
        resp = c.post('/', data={
            'token': slack_token,
            'user_name': 'blurrcat',
            'text': '!debot help',
            'trigger_word': '!debot'
        })
        assert resp.status_code == 200
        resp = json.loads(resp.data)
        assert 'text' in resp


def test_invalid_token(app, slack_token):
    with app.test_client() as c:
        resp = c.post('/', data={
            'token': slack_token + '123',
            'user_name': 'blurrcat',
            'text': '!debot help',
            'trigger_word': '!debot'
        })
        assert resp.status_code == 403

