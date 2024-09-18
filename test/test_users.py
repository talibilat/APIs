import pytest
from app import schemas
from jose import jwt
from app.config import settings
    


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Hello!"
    assert res.status_code == 200




def test_create_user(client):
    res = client.post("/users/", json={"email": "talib1@gmail.com", "password": "t@123"})
    new_user_data = res.json()
    assert res.status_code == 201
    assert "email" in new_user_data
    assert "id" in new_user_data
    assert new_user_data["email"] == "talib1@gmail.com"




def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200  




@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 't@123', 403),
    ('talib1@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 't@123', 422),
    ('talib1@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code