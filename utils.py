import random
import re
import sqlite3
import string
from flask import g

from constants import DATABASE_PATH, TOKEN_SIZE


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


def check_email(email):
    return re.match(r'\S+@\S+\.\S+', email) != None


def check_password(password):
    return len(password) > 0


def get_token():
    symbols = string.ascii_lowercase + string.digits
    return ''.join(random.choice(symbols) for _ in range(TOKEN_SIZE))
