#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
import json
import time
from gevent import spawn, sleep
from gevent.queue import Queue, Empty
import requests


class Notifier(object):
    def __init__(self, app=None):
        self._url = None
        self._channel = None
        self._interval = 1
        self._started = False
        self._q = Queue()
        self._logger = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self._url = app.config['SLACK_INCOMING_WEBHOOK']
        self._channel = app.config['SLACK_CHANNEL']
        self._interval = 1/float(app.config['SLACK_RATE_LIMIT'])
        self._logger = app.logger
        spawn(self._loop)
        app.extensions['slack_notifier'] = self
        self._started = True
        self._logger.info(
            'slack notifier started. min interval: %.1fs; default channel: %s',
            self._interval, self._channel)

    def notify(self, msg, channel=None, now=False):
        """
        send a message to slack.
        The messages are buffered under the hood to avoid hitting Slack API
        rate limit.
        :param msg: message to send
        :param channel: channel to send the message
        """
        if self._started:
            channel = channel if channel else self._channel
            if now:
                self._send(msg, channel)
            else:
                self._q.put((channel, msg))

    def stop(self):
        self._started = False
        self.notify(id(self), None)  # use id as token to stop

    def _send(self, message, channel):
        """
        send to slack incoming webhook
        :param str message: message to send
        :param str channel: channel to send the message in
        :returns: True if send succeeds
        """
        data = {
            'text': message,
            'parse': 'full',
        }
        if channel:
            data['channel'] = channel
        try:
            r = requests.post(self._url, data=json.dumps(data))
        except (requests.ConnectionError, requests.Timeout) as e:
            self._logger.warning('Fail to send slack request: %s', e)
            return False
        else:
            if r.status_code == 200:
                return True
            else:
                self._logger.warning(
                    'Non-200 code returned from slack: %d - %s',
                    r.status_code, r.content
                )
                return False

    def _flush(self):
        """
        flush current queuing messages
        """
        togo = defaultdict(list)
        try:
            while True:
                channel, msg = self._q.get_nowait()
                togo[channel].append(msg)
        except Empty:
            pass
        flushed = []
        for channel, messages in togo.iteritems():
            msg = '\n'.join(messages)
            if not self._send(msg, channel):
                self._logger.error('fail to send message to slack %s - %s',
                                   channel, msg)
            else:
                flushed.append((channel, msg))
        return flushed

    def _loop(self):
        """
        send loop
        """
        last_send = time.time()
        while True:
            top = self._q.peek(block=True)
            if top == id(self):  # stop
                break
            interval = time.time() - last_send
            if interval >= self._interval:
                # flush queue
                flushed = self._flush()
                last_send = time.time()
                self._logger.debug(
                    'flush finished at %.3f: %s', last_send, flushed)
            else:
                sleep(interval)
        self.notify('Bye.')
        self._flush()
