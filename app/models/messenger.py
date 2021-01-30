class MessageModel:
    def __init__(self, json):
        self.text = json.get('text', None)
        self.time = json.get('time', None)
