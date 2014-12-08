import ast
import logging.config
import json
import os
from flask import abort, Flask, request, g
from debot import config
from debot.dispatcher import Dispatcher, HookError


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # production config via env vars
    for k, v in os.environ.items():
        if k.startswith('DEBOT_'):
            try:
                v = ast.literal_eval(v)
            except ValueError:
                pass
            app.config[k[6:]] = v

    logging.config.dictConfig(app.config['LOGGING_CONFIG'])

    dispatcher = Dispatcher(app)
    me = app.config.get("username", "debot")

    @app.before_request
    def token_check():
        if request.form.get('token') != app.config['SLACK_TOKEN']:
            abort(403)

    @app.route("/", methods=['POST'])
    def index():
        g.user = request.form.get('user_name', '').strip()
        message = request.form.get('text', '')
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

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
