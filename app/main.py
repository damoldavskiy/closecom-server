import logging
from flask import Flask, g

from constants import ERROR_LOG_PATH
from controllers import account, bluetooth, messenger
from util import error


app = Flask(__name__)
app.register_blueprint(account.mod)
app.register_blueprint(bluetooth.mod)
app.register_blueprint(messenger.mod)

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
