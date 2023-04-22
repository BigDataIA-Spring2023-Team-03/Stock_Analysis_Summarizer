import pytest
from fastapi.testclient import TestClient
from Authentication import auth
from apis import app
from Util import db_util

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

# user registration tests
def test_register_new_user(test_client):
    email = "testuser@example.com"
    password = "password123"
    service_plan = "basic"
    admin_flag = False

    # make sure user doesn't already exist
    assert not db_util.check_user_exists(email)

    response = test_client.post("/user/register", json={
        "email": email,
        "password": password,
        "service_plan": service_plan,
        "admin_flag": admin_flag
    })

    assert response.status_code == 200
    assert "access_token" in response.json()

    assert db_util.check_user_exists(email)

    db_util.delete_user(email)

def test_register_existing_user(test_client):
    email = "testuser@example.com"
    password = "password123"
    service_plan = "basic"
    admin_flag = False
    db_util.insert_user(email, password, service_plan, admin_flag)

    response = test_client.post("/user/register", json={
        "email": email,
        "password": password,
        "service_plan": service_plan,
        "admin_flag": admin_flag
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "User with that email already exists"

    db_util.delete_user(email)

# user login tests
def test_login_valid_credentials(test_client):
    email = "testuser@example.com"
    password = "password123"
    service_plan = "basic"
    admin_flag = False

    db_util.insert_user(email, auth.get_password_hash(password), service_plan, admin_flag)

    response = test_client.post("/user/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 200
    assert "access_token" in response.json()

    db_util.delete_user(email)

def test_login_invalid_credentials(test_client):
    email = "testuser@example.com"
    password = "password123"
    service_plan = "basic"
    admin_flag = False

    # create user first
    db_util.insert_user(email, auth.get_password_hash(password), service_plan, admin_flag)

    response = test_client.post("/user/login", json={
        "email": email,
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username and/or password"

    # clean up
    db_util.delete_user(email)

# user info tests
def test_user_info_valid_token(test_client):
    email = "testuser@example.com"
    password = "password123"
    service_plan = "basic"
    admin_flag = False

    # create user first
    db_util.insert_user(email, auth.get_password_hash(password), service_plan, admin_flag)

    # log in to get token
    response = test_client.post("/user/login", json={
        "email": email,
        "password": password
    })

    token = response.json()["access_token"]

    # use token to get user info
    response = test_client.get("/user_info", params={'token': token})

    assert response.status_code == 200
    assert response.json()["email"] == email

    # clean up
    db_util.delete_user(email)
