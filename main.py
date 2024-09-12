from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.testclient import TestClient

from services.chat import ChatService

app = FastAPI()


origins = ["http://localhost:3000", "https://ai-assistant-web-beta.vercel.app"]

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


test_client = TestClient(app)


def test_get_messages():
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json()[0].get("id") == 1
    assert response.json()[0].get("sender") == "system"
    assert isinstance(response.json()[0].get("text"), str)
    assert response.json()[0].get("edited") is False


@app.post("/")
async def add_message(text: str):
    try:
        new_messages = chat.add_message(text)
        return new_messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def test_add_message():
    response = test_client.post("/?text=Hello%20World!")
    assert response.status_code == 200

    ## Check if the user message was added to the chat
    assert isinstance(response.json()[0].get("id"), int)
    assert response.json()[0].get("sender") == "user"
    assert response.json()[0].get("text") == "Hello World!"
    assert response.json()[0].get("edited") is False

    ## Check if the system message was added to the chat
    assert isinstance(response.json()[-1].get("id"), int)
    assert response.json()[-1].get("sender") == "system"
    assert isinstance(response.json()[-1].get("text"), str)
    assert response.json()[-1].get("edited") is False


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


def test_update_message():
    ## Create a new message
    response = test_client.post("/?text=Hello%20World!")
    assert response.status_code == 200
    assert isinstance(response.json()[-2].get("id"), int)

    ## Update the message
    message_id = response.json()[-2].get("id")
    response = test_client.put(f"/{message_id}?text=Hello%20World%20Updated!")
    assert response.status_code == 200

    ## Loop through the messages and check if the message was updated
    for message in response.json():
        if message.get("id") == message_id:
            assert message.get("text") == "Hello World Updated!"


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


def test_delete_message():
    ## Create a new message
    response = test_client.post("/?text=Hello%20World!")
    assert response.status_code == 200
    assert isinstance(response.json()[-2].get("id"), int)

    ## Delete the message
    message_id = response.json()[-2].get("id")
    response = test_client.delete(f"/{message_id}")

    ## Loop through the messages and check if the message was deleted
    for message in response.json():
        assert message.get("id") != message_id
