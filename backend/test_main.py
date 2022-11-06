from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_register():
    response = client.post(
        "/api/user/register",
        json={"name": "Кондратьев Андрей Антонович", "email": "kondrandr2004@yandex.ru"}
    )
    assert response.status_code == 204


def test_register_fail():
    response = client.post(
        "/api/user/register",
        json={"name": "Кондратьев Андрей Антонович", "email": "kondrandr2004@yandex.ru"}
    )
    assert response.status_code == 400


def test_login():
    response = client.post(
        "/api/user/login",
        json={"password": "Кондратьев Андрей Антонович", "email": "kondrandr2004@yandex.ru"}
    )
    assert response.status_code != 204


def test_get_analogs():
    response = client.post("/api/user/getAnalogs",
                           json=[{"address": "Москва, проспект 60-летия Октября, 11",
                                   "num_rooms": 1,
                                   "building_segment": "Cтарый жилой фонд",
                                   "building_num_floors": 16,
                                   "building_material": "Панель",
                                   "floor": 10,
                                   "square_flat": 25.0,
                                   "square_kitchen": 10.0,
                                   "has_balcony": False,
                                   "metro_distance": 10,
                                   "condition": "economy"}])
    assert response.status_code == 200


def test_create_user():
    response = client.post(
        "/api/admin/createUser/1"
    )
    assert response.status_code == 200
