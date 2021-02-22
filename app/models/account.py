import re

from constants import MIN_PASSWORD_LENGTH
from util import hash_password


def check_email(email):
    return email != None and re.match(r'\S+@\S+\.\S+', email) != None


def check_password(password):
    return password != None and len(password) >= MIN_PASSWORD_LENGTH


def check_name(name):
    return name != None and len(name) > 0


class Account:
    def __init__(self, json):
        self.email = json.get('email', None)
        self.password = json.get('password', None)
        if check_password(self.password):
            self.password = hash_password(self.password)

    def valid(self):
        return check_email(self.email) and check_password(self.password)


class UserAbout:
    def __init__(self, json):
        self.name = json.get('name', None)

    def valid(self):
        return check_name(self.name)


class User:
    def __init__(self, row):
        self.id = row[0]
        self.email = row[1]
        self.password = row[2]
        self.confirmed = row[3]
        self.name = row[4]
        self.bid = row[5]

    def match(self, account):
        return self.email == account.email and self.password == account.password


class Token:
    def __init__(self, row):
        self.id = row[0]
        self.type = row[1]
        self.token = row[2]
        self.user_id = row[3]
