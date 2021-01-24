from flask import Blueprint, jsonify, request

from utils import check_email, check_password, error, get_db, get_token, ok


app = Blueprint('account', __name__)


@app.route('/account/create', methods=['POST'])
def create():
    content = request.json
    email = content['email']
    password = content['password']

    if not check_email(email) or not check_password(password):
        return error('invalid email or password', 400)

    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT * FROM user WHERE email=?', (email,))
    if cursor.fetchone() != None:
        return error('email already registered', 405)

    cursor.execute('INSERT INTO user (email, password) VALUES (?, ?)', (email, password))
    token = get_token()
    cursor.execute('INSERT INTO token (token, user_id) VALUES (?, ?)', (token, cursor.lastrowid))
    db.commit()

    return {'token': token}


@app.route('/account/auth', methods=['POST'])
def auth():
    content = request.json
    email = content['email']
    password = content['password']

    if not check_email(email) or not check_password(password):
        return error('invalid email or password', 400)

    db = get_db()
    cursor = db.cursor()
 
    cursor.execute('SELECT * FROM user WHERE email=?', (email,))
    row = cursor.fetchone()
    if row == None:
        return error('email not registered', 405)

    if row[2] != password:
        return error('wrong password', 406)

    token = get_token()
    cursor.execute('INSERT INTO token (token, user_id) VALUES (?, ?)', (token, row[0]))
    db.commit()

    return {'token': token}


@app.route('/account/delete', methods=['POST'])
def delete():
    args = request.args
    token = args.get('token')

    db = get_db()
    cursor = db.cursor()
 
    cursor.execute('SELECT * FROM token WHERE token=?', (token,))
    row = cursor.fetchone()
    if row == None:
        return error('invalid token', 401)

    user_id = row[2]
    cursor.execute('DELETE FROM user WHERE id=?', (user_id,))
    db.commit()

    return ok()
