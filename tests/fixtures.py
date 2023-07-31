import pytest

from tests.factories import UserFactory

@pytest.mark.django_db
@pytest.fixture
def auth_user_response(user, client):
    """Фикстура, выполняющая авторизацию зарегистрированного пользователя"""
    password = user.password
    user.set_password(user.password)
    user.save()
    response = client.post("/core/login", data={
        "username": user.username,
        "password": password
    }, content_type='application/json')

    return response
