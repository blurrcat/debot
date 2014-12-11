import ast
import logging.config
import json
import os
from flask import abort, Flask, request, g
from debot import config
from debot.dispatcher import Dispatcher, HookError
from debot.git_plugins import GitPluginsManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # production config via env vars
    for k, v in os.environ.items():
        if k.startswith('DEBOT_'):
            try:
                v = ast.literal_eval(v)
            except (ValueError, SyntaxError):
                pass
            app.config[k[6:]] = v

    logging.config.dictConfig(app.config['LOGGING_CONFIG'])

    plugins_dirs = []
    if app.config.get('EXTRA_PLUGINS_GIT'):
        git_plugins = GitPluginsManager(app)
        plugins_dirs.append(git_plugins.plugins_dir)
    dispatcher = Dispatcher(app, plugins_dirs=plugins_dirs)

    me = app.config.get("username", "debot")

    @app.route("/", methods=['POST'])
    def index():
        if request.form.get('token') != app.config['SLACK_TOKEN']:
            abort(403)
        g.user = request.form.get('user_name', '').strip()
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
        if len(parts) == 2:
            args = parts[1]
        else:
            args = None
        try:
            resp = dispatcher.dispatch(parts[0], args)
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
