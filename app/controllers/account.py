from flask import Blueprint, request

import base
from models.account import Account, UserAbout, User, check_email, check_password
from secrets import secrets
from util import error, get_db, hash_password, log_info, ok, send_email, html_message, html_password_change


mod = Blueprint('account', __name__)


@mod.route('/account/create', methods=['POST'])
def create():
    content = request.json

    account = Account(content)
    if not account.valid():
        return error('invalid email or password', 400)

    user = base.get_user_by_email(account.email)
    if user:
        return error('email already registered', 405)

    user = base.create_user(account)
    access_token = base.create_token(user, 'access')
    confirm_token = base.create_token(user, 'confirm')
    get_db().commit()

    send_email(user.email, 'Account verification', 'http://' + secrets['host_address'] + '/account/confirm?token=' + confirm_token)

    log_info(f'User created {user.email}')

    return {'token': access_token}


@mod.route('/account/confirm', methods=['GET'])
def confirm():
    args = request.args

    confirm_token = args.get('token')

    user = base.get_user_by_token(confirm_token, 'confirm')
    title = 'Account verification'
    if not user:
        return html_message(title, 'Invalid verification token')

    if user.confirmed:
        return html_message(title, 'Account is already verified')

    base.set_user_confirmed(user, 1)
    get_db().commit()

    log_info('User confirmed {user.email}')

    return html_message(title, 'Account has been verified')


@mod.route('/account/recovery', methods=['POST'])
def recovery():
    args = request.args

    email = args.get('email')
    if not check_email(email):
        return error('invalid email', 400)

    user = base.get_user_by_email(email)
    if not user:
        return error('email not registered', 405)

    recovery_token = base.create_token(user, 'recovery')
    get_db().commit()

    send_email(user.email, 'Account recovery', 'http://' + secrets['host_address'] + '/account/recovery_form?token=' + recovery_token)

    log_info(f'Password recovery request {email}')

    return ok()


@mod.route('/account/recovery_form', methods=['GET'])
def recovery_form():
    args = request.args

    recovery_token = args.get('token')

    user = base.get_user_by_token(recovery_token, 'recovery')
    if not user:
        return html_message('Account recovery', 'Invalid recovery token')

    log_info('Password recovery form request {user.email}')

    return html_password_change(recovery_token)


@mod.route('/account/password_change', methods=['POST'])
def password_change():
    content = request.form

    recovery_token = content['token']
    password = hash_password(content['password'])

    title = 'Account recovery'
    if not check_password(password):
        return html_message(title, 'Invalid password')

    user = base.get_user_by_token(recovery_token, 'recovery')
    if not user:
        return html_message(title, 'Invalid recovery token')

    base.set_user_password(user, password)
    get_db().commit()

    log_info('User password changed {user.email}')

    return html_message(title, 'Password has been changed')


@mod.route('/account/auth', methods=['POST'])
def auth():
    content = request.json

    account = Account(content)
    if not account.valid():
        return error('invalid email or password', 400)

    user = base.get_user_by_email(account.email)
    if not user:
        return error('email not registered', 405)

    if not user.match(account):
        return error('wrong password', 406)

    token = base.create_token(user, 'access')
    get_db().commit()

    log_info('Authentication {user.email}')

    return {'token': token}


@mod.route('/account/delete', methods=['POST'])
def delete():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
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

    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)

    base.set_user_about(user, about)
    get_db().commit()

    log_info('User about updated {user.email}')

    return ok()
