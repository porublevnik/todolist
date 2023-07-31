import pytest
from rest_framework import status

@pytest.mark.django_db
def test_signup_password_short(client):
    """Тест провала регистрации при коротком пароле"""
    data = {"username": "johndoe",
            "password": "j*Ki6$s",
            "password_repeat": "j*Ki6$s"}

    response = client.post('/core/signup', data, content_type="application/json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
