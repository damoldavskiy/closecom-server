from flask import Blueprint, request

import base
from util import error, get_db, log_info, ok


mod = Blueprint('bluetooth', __name__)


@mod.route('/bluetooth/user_about')
def user_about():
    args = request.args

    bid = args.get('bid')
    user = base.get_user_by_bid(bid)
    if not user:
        return error('invalid bid', 400)

    log_info(f'User about {user.email}')

    return user.about()


@mod.route('/bluetooth/set_bid', methods=['POST'])
def set_bid():
    args = request.args

    token = args.get('token')
    bid = args.get('bid')
    if len(bid) == 0:
        return error('invalid bid', 400)

    user = base.get_user_by_token(token, 'access')
    if not user:
        return error('invalid token', 401)

    base.set_user_bid(user, bid)
    get_db().commit()

    log_info(f'Set bid: {user.email}, {bid}')

    return ok()
