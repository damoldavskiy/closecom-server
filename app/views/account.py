from flask import Blueprint, request

from app import base
from app.models.user import User
from app.utils import error, get_db, hash_password, log_info, ok


mod = Blueprint('account', __name__)


@mod.route('/account/create', methods=['POST'])
def create():
    content = request.json
    email = content['email']
    password = hash_password(content['password'])

    user = User(email, password)
    if not user.check_email() or not user.check_password():
        return error('invalid email or password', 400)

    record = base.get_user_by_email(user.email)
    if record != None:
        return error('email already registered', 405)

    base.create_user(user)
    token = base.create_token(user)
    get_db().commit()

    log_info('User created {}'.format(email))

    return {'token': token}


@mod.route('/account/auth', methods=['POST'])
def auth():
    content = request.json
    email = content['email']
    password = hash_password(content['password'])

    user = User(email, password)
    if not user.check_email() or not user.check_password():
        return error('invalid email or password', 400)

    record = base.get_user_by_email(user.email)
    if record == None:
        return error('email not registered', 405)

    if user.password != record.password:
        return error('wrong password', 406)

    token = base.create_token(record)
    get_db().commit()

    log_info('Authentication {}'.format(email))

    return {'token': token}


@mod.route('/account/delete', methods=['POST'])
def delete():
    args = request.args
    token = args.get('token')

    user = base.get_user_by_token(token)
    if user == None:
        return error('invalid token', 401)

    base.delete_user(user)
    get_db().commit()

    log_info('User deleted {}'.format(user.email))

    return ok()
