from flask import Blueprint, request

import base
from models.account import Account, UserAbout, User
from util import error, get_db, log_info, ok


mod = Blueprint('account', __name__)


@mod.route('/account/create', methods=['POST'])
def create():
    content = request.json

    account = Account(content)
    if not account.valid():
        return error('invalid email or password', 400)

    user = base.get_user_by_email(account.email)
    if user != None:
        return error('email already registered', 405)

    user = base.create_user(account)
    token = base.create_token(user)
    get_db().commit()

    log_info(f'User created {user.email}')

    return {'token': token}


@mod.route('/account/auth', methods=['POST'])
def auth():
    content = request.json

    account = Account(content)
    if not account.valid():
        return error('invalid email or password', 400)

    user = base.get_user_by_email(account.email)
    if user == None:
        return error('email not registered', 405)

    if not user.match(account):
        return error('wrong password', 406)

    token = base.create_token(user)
    get_db().commit()

    log_info('Authentication {user.email}')

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

    log_info('User deleted {user.email}')

    return ok()


@mod.route('/account/set_about', methods=['POST'])
def set_about():
    args = request.args
    content = request.json

    token = args.get('token')
    about = UserAbout(content)
    if not about.valid():
        return error('invalid about section', 405)

    user = base.get_user_by_token(token)
    if user == None:
        return error('invald token', 401)

    base.set_user_about(user, about)
    get_db().commit()

    log_info('User about updated {user.email}')

    return ok()
