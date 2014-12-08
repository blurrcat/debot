import ast
import json
import os
from flask import Flask, request
from debot import config
from debot.dispatcher import Dispatcher


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

    dispatcher = Dispatcher(app)

    @app.route("/", methods=['POST'])
    def index():
        me = app.config.get("username", "slask")
        icon = app.config.get("icon", ":poop:")

        # ignore message we sent; the outgoing webhook should only POST when
        # message is prefixed: "!command *args"
        from_user = request.form.get("user_name", "").strip()
        message = request.form.get('message', '')
        if from_user == me or from_user.lower() == "slackbot":
            return ""
        parts = message.split()
        if message.startswith(app.config['DEBOT_COMMAND_KEYWORD']):
            command = parts[1]
            args = parts[2:]
        elif message.startswith(app.config['DEBOT_COMMAND_PREFIX']):
            command = parts[0].lstrip(app.config['DEBOT_COMMAND_PREFIX'])
            args = parts[1:]
        else:
            return ""

        resp = dispatcher.dispatch(command, args)
        if not resp:
            return ""

        return json.dumps({
            "text": resp,
            "username": me,
            "icon_emoji": icon,
            "parse": "full",
        })

if __name__ == "__main__":
    create_app().run(debug=True)
