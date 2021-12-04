from app import schemas

from .database import client, session


def test_root(client):
    r = client.get("/")

    assert r.json().get("message") == ":)"
    assert r.status_code == 200


def test_create_user(client):
    r = client.post("/users/", json={"email": "hei3@hei.no", "password": "hei123"})

    new_user = schemas.UserOut(**r.json())

    assert new_user.email == "hei3@hei.no"

    assert r.status_code == 201
