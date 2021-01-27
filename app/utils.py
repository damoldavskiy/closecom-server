import sqlite3
from flask import current_app, g
from hashlib import sha256
from os import urandom

from app.constants import DATABASE_PATH, TOKEN_SIZE


def log_info(message):
    current_app.logger.info(message)


def get_token():
    return urandom(TOKEN_SIZE).hex()


def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()


def ok():
    return {'message': 'ok'}


def error(message, code):
    return {'error_message': message}, code


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
        db.execute('PRAGMA foreign_keys = ON')
    return db
