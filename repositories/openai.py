import os

from openai import OpenAI
from dotenv import load_dotenv

from entities.message import MessageEntity

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class OpenAIRepository:
    def initiate_chat(self):
        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful assistant named Ava.
                        You are here to help the customer troubleshoot their device. 
                        The customer will describe the issue they are experiencing, and you will provide a solution. 
                        The solution should be short and to the point.
                        You should start the conversation by being cordial and asking the user's name.
                        Answers should be short.""",
                }
            ],
        )

        message = MessageEntity(1, chat.choices[0].message.content, "system")

        return message

    def get_response(self, prompt: str, prev_mess_id: int):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                }
            ],
        )

        message = MessageEntity(
            prev_mess_id + 1, response.choices[0].message.content, "system"
        )

        return message
