class MessageEntity:
    def __init__(self, id: int, text: str, sender: str):
        self.id = id
        self.text = text
        self.sender = sender
        self.edited = False

    def get_text(self):
        return self.text

    def get_sender(self):
        return self.sender

    def update_text(self, text):
        self.text = text
        self.edited = True
