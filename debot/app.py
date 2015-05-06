from gevent import monkey
monkey.patch_all()
import ast
import logging.config
import json
import os
from flask import abort, Flask, request, g
from debot import config
from debot.dispatcher import HookError
from debot.extensions import notifier, git_plugin_manager, dispatcher


def create_app():
    app = Flask('debot')
    app.config.from_object(config)
    # production config via env vars
    for k, v in os.environ.items():
        if k.startswith('DEBOT_'):
            try:
                v = ast.literal_eval(v)
            except (ValueError, SyntaxError):
                pass
            app.config[k[6:]] = v
    # logging config
    # logging.config.dictConfig(app.config['LOGGING_CONFIG'])

    if not app.config['ADMINS']:
        app.logger.warning(
            'No admin configured; Plugins decorated with "admin_required" ' +
            'can not be called')

    # slack notifier
    if app.config.get('SLACK_INCOMING_WEBHOOK'):
        notifier.init_app(app)

    # plugins
    plugins_dirs = []
    if app.config.get('EXTRA_PLUGINS_GIT'):
        git_plugin_manager.init_app(app)
        plugins_dirs.append(git_plugin_manager.plugins_dir)
    dispatcher.init_app(app, plugins_dirs=plugins_dirs)

    me = app.config.get("username", "debot")

    @app.route("/", methods=['POST'])
    def index():
        if request.form.get('token') != app.config['SLACK_TOKEN']:
            abort(403)
        g.user = request.form.get('user_name', '').strip()
        g.channel = '#%s' % request.form.get('channel_name', '').strip()
        message = request.form.get('text', '')
        app.logger.info('msg "%s" from user "%s"', message, g.user)
        # ignore message we sent
        if g.user == me or g.user.lower() == "slackbot":
            return ""
        trigger_word = request.form.get('trigger_word', '')
        if trigger_word:
            message = message.lstrip(trigger_word)
        message = message.strip()
        parts = message.split(' ', 1)
        try:
            args = parts[1]
        except IndexError:
            args = None
        try:
            resp = dispatcher.dispatch(parts[0].lower(), args)
            color = 'good'
        except HookError as e:
            resp = e.message
            color = 'danger'
        if not resp:
            return ""
        else:
            return json.dumps({
                'text': resp,
                'parse': 'full',
                'color': color
            })

    @app.route('/_health')
    def health():
        return 'ok'

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
