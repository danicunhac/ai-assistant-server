from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_messages():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()[0].get("id") == 1
    assert response.json()[0].get("sender") == "system"
    assert isinstance(response.json()[0].get("text"), str)
    assert response.json()[0].get("edited") is False

def test_add_message():
    response = client.post("/?text=Hello%20World!")
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
   
def test_update_message():
    ## Create a new message
    response = client.post("/?text=Hello%20World!")
    assert response.status_code == 200
    assert isinstance(response.json()[-2].get("id"), int)

    ## Update the message
    message_id = response.json()[-2].get("id")
    response = client.put(f"/{message_id}?text=Hello%20World%20Updated!")
    assert response.status_code == 200

    ## Loop through the messages and check if the message was updated
    for message in response.json():
        if message.get("id") == message_id:
            assert message.get("text") == "Hello World Updated!"



def test_delete_message():
    ## Create a new message
    response = client.post("/?text=Hello%20World!")
    assert response.status_code == 200
    assert isinstance(response.json()[-2].get("id"), int)

    ## Delete the message
    message_id = response.json()[-2].get("id")
    response = client.delete(f"/{message_id}")

    ## Loop through the messages and check if the message was deleted
    for message in response.json():
        assert message.get("id") != message_id