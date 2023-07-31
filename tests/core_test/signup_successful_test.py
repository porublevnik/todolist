import pytest
from rest_framework import status

@pytest.mark.django_db
def test_signup(client):
    """Тест успешной авторизации нового пользователя"""
    data = {"username": "johndoe",
            "password": "j*Ki6$vN",
            "password_repeat": "j*Ki6$vN"}

    expected_response = {
        "username": "johndoe",
        "first_name": "",
        "last_name": "",
        "email": "",
        'id': 2
    }

    response = client.post('/core/signup', data, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_response
