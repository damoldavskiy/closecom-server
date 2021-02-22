import logging
from flask import Flask, g
from flask_mail import Mail

from constants import ERROR_LOG_PATH, MAIL_SERVER, MAIL_PORT
from controllers import account, bluetooth, messenger
from secrets import secrets
from util import error


app = Flask(__name__)
app.register_blueprint(account.mod)
app.register_blueprint(bluetooth.mod)
app.register_blueprint(messenger.mod)

app.config.update(dict(
    MAIL_SERVER = MAIL_SERVER,
    MAIL_PORT = MAIL_PORT,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = secrets['mail_username'],
    MAIL_PASSWORD = secrets['mail_password']
))

mail = Mail(app)

logging.basicConfig(filename=ERROR_LOG_PATH,
                    level=logging.INFO,
                    format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
                    datefmt='%F %X %z')


@app.errorhandler(500)
def internal_error(exception):
    return error('internal server error', 500)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
