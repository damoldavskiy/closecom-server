import sqlite3
from flask import current_app, g
from flask_mail import Mail, Message
from hashlib import sha256
from os import urandom

from constants import DATABASE_PATH, TOKEN_SIZE


def log_info(message):
    current_app.logger.info(message)


def send_email(recipient, title, text):
    message = Message(title, sender='donotreply@closecom.org', recipients=[recipient])
    message.body = text
    with current_app.app_context():
        mail = Mail()
        mail.send(message)
    

def get_token():
    return urandom(TOKEN_SIZE).hex()


def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()


def ok():
    return {'message': 'ok'}


def error(message, code):
    return {'error_message': message}, code


def html_message(title, message):
    return '<html><head><title>' + title + '</title><style>body{color:#2D3CC8;font-family:sans-serif;'\
           'text-align:center;margin-top:50px;font-size:24;}</style></head><body>' + message + '</body></html>'


def html_password_change(token):
    return '<html><head><title>Account recovery</title><style>body{color:#2D3CC8;font-family:sans-serif;'\
           'text-align:center;margin-top:50px;font-size:24;}input{margin-top:20px;margin-left:10px;margin-right:10px;}'\
           '</style></head><body>Enter new password<form action="/account/change_password" method="post"><input type="password" name="password">'\
           '<input type="submit" value="Confirm"><input type="hidden" name="token" value="' + token + '"></form></body></html>'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
        db.execute('PRAGMA foreign_keys = ON')
    return db
