from typing import Union


from fastapi import FastAPI, HTTPException

from services.chat import ChatService

app = FastAPI()

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
        chat.add_message(text)
        return chat.get_messages()
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
