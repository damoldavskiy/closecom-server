from flask import Blueprint, request

import base
from util import error, get_db, log_info, ok


mod = Blueprint('messenger', __name__)


@mod.route('/messenger/chats')
def chats():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)
    return error('not implemented', 404)


@mod.route('/messenger/chats_history')
def chats_history():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)
    return error('not implemented', 404)


@mod.route('/messenger/send_message', methods=['POST'])
def send_message():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)
    return error('not implemented', 404)


@mod.route('/messenger/delete_message', methods=['POST'])
def delete_message():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)
    return error('not implemented', 404)


@mod.route('/messenger/delete_chat', methods=['POST'])
def delete_chat():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)
    return error('not implemented', 404)
