#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '-s', '--scheme', choices=('http', 'https'), default='http')
parser.add_argument('-H', '--host', default='localhost')
parser.add_argument('-p', '--port', type=int, default=5000)
parser.add_argument('-T', '--token', default='slack_token')
parser.add_argument('text')
parser.add_argument('-t', '--trigger', default='!')
parser.add_argument('-u', '--user', default='blurrcat')
args = parser.parse_args()
resp = requests.post('%s://%s:%s' % (args.scheme, args.host, args.port), data={
    'token': args.token,
    'user_name': args.user,
    'text': args.text,
    'trigger_word': args.trigger
})
print(json.loads(resp.content)['text'])
