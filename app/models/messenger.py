class Chat:
    def __init__(self, row):
        self.id = row[0]
        self.type = row[1]


class MessageModel:
    def __init__(self, json):
        self.text = json.get('text', None)
        self.time = json.get('time', None)

    def valid(self):
        return type(self.text) == str and len(self.text) > 0


class Message:
    def __init__(self, row):
        self.id = row[0]
        self.chat_id = row[1]
        self.user_id = row[2]
        self.time = row[3]
        self.text = row[4]
