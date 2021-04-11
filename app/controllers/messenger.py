import json
from flask import Blueprint, request

import base
from models.messenger import MessageModel
from util import error, get_db, log_info, ok


mod = Blueprint('messenger', __name__)


@mod.route('/messenger/chats')
def chats():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)

    return {'chats': base.get_chats(user)}


@mod.route('/messenger/chat_history')
def chat_history():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)

    chat_id = args.get('chat_id')
    if chat_id is None:
        return error('invalid chat id', 400)

    if not base.is_user_in_chat(user, chat_id):
        return error('invalid chat id', 400)

    return base.get_chat_history(chat_id)


@mod.route('/messenger/send_message', methods=['POST'])
def send_message():
    args = request.args
    content = request.json

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)

    chat_id = args.get('chat_id')
    if not base.is_user_in_chat(user, chat_id):
        return error('invalid chat id', 400)

    message = MessageModel(content)
    if not message.valid():
        return error('invalid message', 405)

    base.send_message(user, chat_id, message)
    get_db().commit()
    return ok()


@mod.route('/messenger/send_private', methods=['POST'])
def send_private():
    args = request.args
    content = request.json

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invald token', 401)

    recipient_id = args.get('user_id')
    recipient = base.get_user_by_id(recipient_id)
    if recipient is None:
        return error('invalid user id', 400)

    message = MessageModel(content)
    if not message.valid():
        return error('invalid message', 405)

    base.send_private(user, recipient, message)
    get_db().commit()
    return ok()


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
