import pytest
from app import database, schemas
from jose import jwt
from .database import client, session
from app.config import settings


def test_create_user(client):
    r = client.post("/users/", json={"email": "hei3@hei.no", "password": "hei123"})

    new_user = schemas.UserOut(**r.json())

    assert new_user.email == "hei3@hei.no"

    assert r.status_code == 201


def test_login_user(client, test_user):
    r = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**r.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )

    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"

    assert r.status_code == 200


# BRUK PARAMTERIZE!
@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "hei123", 403),
        ("hei3@hei.no", "hei123", 200),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "hei123", 422),
        ("hei3@hei.no", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    r = client.post("/login", data={"username": email, "password": password})

    assert r.status_code == status_code
    # assert r.json().get("detail") == "Invalid credentials"
