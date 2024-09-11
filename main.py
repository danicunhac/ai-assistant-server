from typing import Union


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.chat import ChatService

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

chat = ChatService()


@app.get("/")
async def get_messages():
    try:
        if not chat.get_messages():
            await chat.start_chat()

        return chat.get_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/")
async def add_message(text: str):
    try:
        new_messages = chat.add_message(text)
        return new_messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/{id}")
async def update_message(id: int, text: str):
    try:
        selected_message = chat.get_message(id)

        if selected_message is None:
            raise HTTPException(status_code=404, detail="Message not found")

        if selected_message.get_sender() == "system":
            raise HTTPException(status_code=400, detail="Cannot update system messages")

        if chat.update_message(id, text):
            return chat.get_messages()
        else:
            raise HTTPException(status_code=404, detail="Message not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/{id}")
async def delete_message(id: int):
    try:
        selected_message = chat.get_message(id)

        if selected_message is None:
            raise HTTPException(status_code=404, detail="Message not found")

        if selected_message.get_sender() == "system":
            raise HTTPException(status_code=400, detail="Cannot delete system messages")

        if chat.delete_message(id):
            return chat.get_messages()
        else:
            raise HTTPException(status_code=404, detail="Message not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
