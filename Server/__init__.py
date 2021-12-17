import os

from flask import Flask, request
from flask_mail import Mail, Message

from Server.info import username, passw


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    # from . import auth
    # app.register_blueprint(auth.bp)

    from . import api
    app.register_blueprint(api.bp)
    app.add_url_rule("/", endpoint="index")

    app.config['MAIL_SERVER'] = 'mail.mohsseni.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = username
    app.config['MAIL_PASSWORD'] = passw
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    email = Mail(app)

    @app.route("/mail")
    def mail():
        if request.method == "GET":
            if "msg" in request.args:
                message = request.args["msg"]
                msg = Message('Warning from IoT Project', sender=username, recipients=['vahid.mohsseni@student.oulu.fi'])
                msg.body = "Hey Admin, \n " + message + "\n\n end of message!"
                email.send(msg)
                return "Message sent!"

    return app

