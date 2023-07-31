import pytest
from rest_framework import status

@pytest.mark.django_db
def test_signup_password_short(client):
    """Тест провала регистрации при простом пароле"""
    data = {"username": "johndoe",
            "password": "1111111111",
            "password_repeat": "1111111111"}

    response = client.post('/core/signup', data, content_type="application/json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
