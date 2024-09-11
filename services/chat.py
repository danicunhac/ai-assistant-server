import uuid

from repositories.openai import OpenAIRepository
from entities.message import MessageEntity


class ChatService:
    def __init__(self):
        self.id = str(uuid.uuid4())  # type: str
        self.user_name = None  # type: str
        self.messages = []  # type: list[MessageEntity]

    async def start_chat(self):
        initial_message = OpenAIRepository().initiate_chat()

        print(f"Initial message: {initial_message.get_text()}")

        self.messages.append(initial_message)

        return self.messages

    def add_message(self, text: str):
        new_message_id = len(self.messages) + 1

        user_message = MessageEntity(new_message_id, text, "user")

        self.messages.append(user_message)

        new_message = OpenAIRepository().get_response(text, new_message_id)

        self.messages.append(new_message)

    def get_messages(self):
        return self.messages

    def get_message(self, id):
        for message in self.messages:
            if message.id == id:
                return message
        return None

    def update_message(self, id, text):
        for message in self.messages:
            if message.id == id:
                message.update_text(text)
                return True
        return False

    def delete_message(self, id):
        for message in self.messages:
            if message.id == id:
                self.messages.remove(message)
                return True
        return False
