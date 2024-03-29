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

    chats = base.get_chats(user)
    for chat in chats:
        if chat['type'] == 'private':
            recipients = [r for r in chat['users'] if r['id'] != user.id]
            chat['name'] = recipients[0]['email'] if len(recipients) > 0 else 'Account deleted'

    log_info(f'Get chats for user {user.email}')

    return {'chats': chats}


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

    chat = base.get_chat_history(chat_id)
    if chat['type'] == 'private':
        recipients = [r for r in chat['users'] if r['id'] != user.id]
        chat['name'] = recipients[0]['email'] if len(recipients) > 0 else 'Account deleted'

    log_info(f'Get chat history for user {user.email}')

    return chat


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

    return {'chat_id': chat_id}


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

    message_id = args.get('message_id')
    message = base.get_message_by_id(message_id)
    if not message or message.user_id != user.id:
        return error('invalid message id', 400)

    base.delete_message(message)
    get_db().commit()

    log_info(f'Deleted message {message.text} by user {user.email}')

    return ok()


@mod.route('/messenger/delete_chat', methods=['POST'])
def delete_chat():
    args = request.args

    token = args.get('token')
    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invalid token', 401)

    chat_id = args.get('chat_id')
    if not base.is_user_in_chat(user, chat_id):
        return error('invalid chat id', 400)

    chat = base.get_chat_by_id(chat_id)
    if chat.type == 'private':
        base.delete_chat(chat)
        log_info(f'Deleted private chat {chat_id} by user {user.email}')
    else:
        base.delete_membership(user, chat)
        log_info(f'Deleted membership in chat {chat_id} by user {user.email}')
    get_db().commit()

    return ok()
