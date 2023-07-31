import pytest
from rest_framework import status

@pytest.mark.django_db
def test_signup_passwords_unmatching(client):
    """Тест провала регистрации при несовпадении введенных паролей"""
    data = {"username": "johndoe",
            "password": "j*Ki6$vN",
            "password_repeat": "j*Ki6$vNa"}

    response = client.post('/core/signup', data, content_type="application/json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
