from fastapi.testclient import TestClient
from chatdraw.app import app
from chatdraw.db import Sketch, get_db_session 

client = TestClient(app)



def test_app():
    test_concept = "giraffe" # part of db seed
    json_data = {
        "message": test_concept,
        "context": "greeting_chooseconcept"
    }
    header = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    response = client.post("/", json=json_data, headers=header)
    assert response.status_code == 200
    assert response.json()["next_context"] == f"greeting_{test_concept},2"
    assert response.json()["response"][0]["content"] == f"What a good choice. Lets draw a {test_concept}."
    
