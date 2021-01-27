import re


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def check_email(self):
        return re.match(r'\S+@\S+\.\S+', self.email) != None

    def check_password(self):
        return len(self.password) > 0
