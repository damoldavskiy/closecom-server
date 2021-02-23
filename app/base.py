from models.account import User, Token
from util import get_db, get_token


USER_COLUMNS = 'id, email, password, confirmed, name, bid'
TOKEN_COLUMNS = 'id, type, token, user_id'
CHAT_COLUMNS = 'id, type'
MEMBERSHIP_COLUMNS = 'user_id, chat_id'
MESSAGE_COLUMNS = 'id, chat_id, user_id, time, text'


def get_user_by_email(email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'SELECT {USER_COLUMNS} FROM user WHERE email=?', (email,))
    row = cursor.fetchone()
    if row == None:
        return None
    return User(row)


def get_user_by_token(token, token_type):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'SELECT {TOKEN_COLUMNS} FROM token WHERE token=? AND type=?', (token,token_type))
    row = cursor.fetchone()
    if row == None:
        return None
    token = Token(row)
    cursor.execute(f'SELECT {USER_COLUMNS} FROM user WHERE id=?', (token.user_id,))
    row = cursor.fetchone()
    return User(row)


def get_user_by_bid(bid):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'SELECT {USER_COLUMNS} FROM user WHERE bid=?', (bid,))
    row = cursor.fetchone()
    if row == None:
        return None
    return User(row)


def create_user(account):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO user (email, password) VALUES (?, ?)', (account.email, account.password))
    cursor.execute(f'SELECT {USER_COLUMNS} FROM user WHERE id=?', (cursor.lastrowid,))
    return User(cursor.fetchone())


def delete_user(user):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM user WHERE email=?', (user.email,))


def create_token(user, token_type):
    db = get_db()
    cursor = db.cursor()
    token = get_token()
    cursor.execute('INSERT INTO token (token, type, user_id) VALUES (?, ?, ?)', (token, token_type, user.id))
    return token


def set_user_password(user, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE user SET password=? WHERE id=?', (password, user.id))


def set_user_confirmed(user, confirmed):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE user SET confirmed=? WHERE id=?', (confirmed, user.id))


def set_user_about(user, about):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE user SET name=? WHERE id=?', (about.name, user.id))


def set_user_bid(user, bid):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE user SET bid=? WHERE id=?', (bid, user.id))
