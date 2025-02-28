from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_user_creation():
    signup_data = {
            "username": "user123",
            "email": "user123@gmail.com",
            "full_name": "user123",
            "password": "test123"
    }
    response = client.post("/users/create", json=signup_data)

    assert response.status_code == 201


def test_restaurant_creation():
    restaurant_data = {
        "name": "testrestaurant"
    }
    response = client.post("/restaurants", json=restaurant_data)

    assert response.status_code == 200


def test_create_restaurant_already_exists():
    restaurant_data = {
        "name": "testrestaurant"
    }
    response = client.post("/restaurants", json=restaurant_data)

    assert response.status_code == 400


def test_menu_creation():
    menu_data = {
        "restaurant_id": 1,
        "items": "string"
    }
    response = client.post("/menus", json=menu_data)

    assert response.status_code == 201


def test_menu_get():
    response = client.get("/menus/today")

    assert response.status_code == 201


def test_vote():
    vote_data = {
        "employee_id": 1,
        "menu_id": 1
    }
    response = client.post("/vote", json=vote_data)

    assert response.status_code == 201
