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
        return error('invalid token', 401)

    log_info(f'Get chats for user {user.email}')

    return {'chats': base.get_chats(user)}


@mod.route('/messenger/chat_history')
def chat_history():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invalid token', 401)

    chat_id = args.get('chat_id')
    if chat_id is None:
        return error('invalid chat id', 400)

    if not base.is_user_in_chat(user, chat_id):
        return error('invalid chat id', 400)

    log_info(f'Get chat history for user {user.email}')

    return base.get_chat_history(chat_id)


@mod.route('/messenger/start_dialog', methods=['POST'])
def start_dialog():
    args = request.args
    content = request.json

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invalid token', 401)

    recipient_id = args.get('user_id')
    if recipient_id is None:
        return error('invalid user id', 400)

    recipient = base.get_user_by_id(recipient_id)
    if recipient is None:
        return error('invalid user id', 400)

    if recipient.id == user.id:
        return error('self chats are not supported', 400)

    message = MessageModel(content)
    if not message.valid():
        return error('invalid message', 405)

    log_info(f'Start dialog by user {user.email} for user {recipient.email}')

    chat_id = base.get_private_chat_id(user, recipient)
    if not chat_id:
        return error('chat already started', 402)

    base.send_message(user, chat_id, message)
    get_db().commit()

    return ok()


@mod.route('/messenger/user_search')
def user_search():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invalid token', 401)

    email = args.get('email')
    if email is None:
        return error('invalid email to search', 400)

    log_info(f'Search by user {user.email} for {email}')

    return {'users': base.user_search(user, email)}


@mod.route('/messenger/create_chat', methods=['POST'])
def create_chat():
    args = request.args
    content = request.json

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invalid token', 401)

    chat_name = args.get('name')
    if type(chat_name) is not str or len(chat_name) == 0:
        return error('invalid chat name', 402)

    user_ids = content.get('users', None)
    if type(user_ids) is not list or len(user_ids) == 0:
        return error('invalid users list', 405)

    users = []
    for user_id in user_ids:
        current_user = base.get_user_by_id(user_id)
        if current_user is None:
            return error('invalid user id in list', 402)
        users.append(current_user)

    chat_id = base.create_chat(user, users, chat_name)
    get_db().commit()

    log_info(f'Create public chat by user {user.email}')

    return {'chat_id': chat_id}


@mod.route('/messenger/send_message', methods=['POST'])
def send_message():
    args = request.args
    content = request.json

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invalid token', 401)

    chat_id = args.get('chat_id')
    if not base.is_user_in_chat(user, chat_id):
        return error('invalid chat id', 400)

    message = MessageModel(content)
    if not message.valid():
        return error('invalid message', 405)

    base.send_message(user, chat_id, message)
    get_db().commit()

    log_info(f'Send message {message.text} by user {user.email}')

    return ok()


@mod.route('/messenger/delete_message', methods=['POST'])
def delete_message():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invalid token', 401)
    return error('not implemented', 404)


@mod.route('/messenger/delete_chat', methods=['POST'])
def delete_chat():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invalid token', 401)
    return error('not implemented', 404)
