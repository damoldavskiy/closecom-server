from app.models.user import User
from app.utils import get_db, get_token


def get_user_by_email(email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, email, password FROM user WHERE email=?', (email,))
    row = cursor.fetchone()
    if row == None:
        return None
    user = User(row[1], row[2])
    user.id = row[0]
    return user


def get_user_by_token(token):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, token, user_id FROM token WHERE token=?', (token,))
    row = cursor.fetchone()
    if row == None:
        return None
    user_id = row[2]
    cursor.execute('SELECT id, email, password FROM user WHERE id=?', (user_id,))
    row = cursor.fetchone()
    user = User(row[1], row[2])
    user.id = row[0]
    return user


def create_user(user):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO user (email, password) VALUES (?, ?)', (user.email, user.password))
    user.id = cursor.lastrowid   


def delete_user(user):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM user WHERE email=?', (user.email,))


def create_token(user):
    db = get_db()
    cursor = db.cursor()
    token = get_token()
    cursor.execute('INSERT INTO token (token, user_id) VALUES (?, ?)', (token, user.id))
    return token
