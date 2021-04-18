from models.account import User, Token
from models.messenger import Chat, Message
from util import get_db, get_token


def columns(names, table):
    return ', '.join([f'{table}.{column}' for column in names.split()])


USER_COLUMNS = columns('id email password confirmed name bid', 'user')
TOKEN_COLUMNS = columns('id type token user_id', 'token')
CHAT_COLUMNS = columns('id type name', 'chat')
MEMBERSHIP_COLUMNS = columns('user_id chat_id', 'membership')
MESSAGE_COLUMNS = columns('id chat_id user_id time text', 'message')


def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'SELECT {USER_COLUMNS} FROM user WHERE id=?', (user_id,))
    row = cursor.fetchone()
    if row == None:
        return None
    return User(row)


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
    cursor.execute(f'SELECT {TOKEN_COLUMNS} FROM token WHERE token=? AND type=?', (token, token_type))
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


def get_chat_by_id(chat_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'SELECT {CHAT_COLUMNS} FROM chat WHERE id=?', (chat_id,))
    row = cursor.fetchone()
    if row == None:
        return None
    return Chat(row)


def get_message_by_id(message_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f'SELECT {MESSAGE_COLUMNS} FROM message WHERE id=?', (message_id,))
    row = cursor.fetchone()
    if row == None:
        return None
    return Message(row)


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


def get_chats(user):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT chat_id FROM membership WHERE user_id=?', (user.id,))
    rows = cursor.fetchall()
    chats = []
    for row in rows:
        chat_id = row[0]

        cursor.execute(f'SELECT {USER_COLUMNS} FROM user JOIN membership ON user.id=membership.user_id WHERE chat_id=?', (chat_id,))
        user_rows = cursor.fetchall()
        users = []
        for user_row in user_rows:
            users.append(User(user_row).about())

        cursor.execute(f'SELECT DISTINCT {USER_COLUMNS} FROM user JOIN message ON user.id=message.user_id WHERE message.chat_id=?', (chat_id,))
        sender_rows = cursor.fetchall()
        senders = []
        for sender_row in sender_rows:
            senders.append(User(sender_row).about())

        cursor.execute(f'SELECT {MESSAGE_COLUMNS} FROM message WHERE chat_id=? ORDER BY id DESC LIMIT 1', (chat_id,))
        message_row = cursor.fetchone()
        message = Message(message_row).__dict__ if message_row is not None else None

        cursor.execute(f'SELECT {CHAT_COLUMNS} FROM chat WHERE id=?', (chat_id,))
        chat_row = cursor.fetchone()
        chat = Chat(chat_row)

        chats.append({'chat_id': chat_id, 'type': chat.type, 'name': chat.name, 'users': users, 'senders': senders, 'latest_message': message})
    return chats


def create_chat(creator, users, chat_name):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('INSERT INTO chat (type, name) VALUES ("public", ?)', (chat_name,))
    chat_id = cursor.lastrowid

    for user in [creator, *users]:
        cursor.execute('INSERT INTO membership (user_id, chat_id) VALUES (?, ?)', (user.id, chat_id))

    return chat_id


def is_user_in_chat(user, chat_id):
     db = get_db()
     cursor = db.cursor()
     cursor.execute(f'SELECT EXISTS(SELECT {MEMBERSHIP_COLUMNS} FROM membership WHERE user_id=? AND chat_id=?) AS found', (user.id, chat_id))
     row = cursor.fetchone()
     return bool(row[0])


def get_chat_history(chat_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(f'SELECT {USER_COLUMNS} FROM user JOIN membership ON user.id=membership.user_id WHERE chat_id=?', (chat_id,))
    user_rows = cursor.fetchall()
    users = []
    for user_row in user_rows:
        users.append(User(user_row).about())

    cursor.execute(f'SELECT DISTINCT {USER_COLUMNS} FROM user JOIN message ON user.id=message.user_id WHERE message.chat_id=?', (chat_id,))
    sender_rows = cursor.fetchall()
    senders = []
    for sender_row in sender_rows:
        senders.append(User(sender_row).about())

    cursor.execute(f'SELECT {MESSAGE_COLUMNS} FROM message WHERE chat_id=? ORDER BY id', (chat_id,))
    message_rows = cursor.fetchall()
    messages = []
    for message_row in message_rows:
        messages.append(Message(message_row).__dict__)

    cursor.execute(f'SELECT {CHAT_COLUMNS} FROM chat WHERE id=?', (chat_id,))
    chat_row = cursor.fetchone()
    chat = Chat(chat_row)

    return {'users': users, 'senders': senders, 'type': chat.type, 'name': chat.name, 'messages': messages}


def send_message(user, chat_id, message):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO message (chat_id, user_id, time, text) VALUES (?, ?, ?, ?)', (chat_id, user.id, message.time, message.text))


def get_private_chat_id(sender, recipient):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT EXISTS(SELECT chat.id FROM chat JOIN membership AS sender_ms ON chat.id=sender_ms.chat_id JOIN membership AS recipient_ms ON chat.id=recipient_ms.chat_id WHERE type="private" AND sender_ms.user_id=? AND recipient_ms.user_id=?) AS found', (sender.id, recipient.id))
    row = cursor.fetchone()

    if row[0]:
        return 0

    cursor.execute('INSERT INTO chat (type) VALUES ("private")')
    chat_id = cursor.lastrowid
    cursor.execute('INSERT INTO membership (user_id, chat_id) VALUES (?, ?)', (sender.id, chat_id))
    cursor.execute('INSERT INTO membership (user_id, chat_id) VALUES (?, ?)', (recipient.id, chat_id))
    return chat_id


def user_search(requester, email):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(f'SELECT {USER_COLUMNS} FROM user WHERE email LIKE ? LIMIT 10', (f'%{email}%',))
    user_rows = cursor.fetchall()
    users = []
    for user_row in user_rows:
        user = User(user_row)
        if user.email != requester.email:
            users.append(user.about())

    return users


def delete_message(message):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM message WHERE id=?', (message.id,))


def delete_chat(chat):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM chat WHERE id=?', (chat.id,))


def delete_membership(user, chat):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM membership WHERE user_id=? AND chat_id=?', (user.id, chat.id))

    cursor.execute('SELECT EXISTS(SELECT user_id FROM membership WHERE chat_id=?) AS found', (chat.id,))
    row = cursor.fetchone()

    if row[0]:
        return

    delete_chat(chat)
