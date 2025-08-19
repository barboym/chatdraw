from fastapi.testclient import TestClient
import pytest
from chatdraw.chatdraw.app import app 

client = TestClient(app)



def test_app():
    json_data = {
        "message": "giraffe",
        "context": "greeting_chooseconcept"
    }
    header = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    response = client.post("/", json=json_data, headers=header)
    assert response.status_code == 200
    assert response.json()["next_context"] == 'greeting_giraffe,2'
    assert response.json()["response"][0]["content"] == 'What a good choice. Lets draw a giraffe.'
    
