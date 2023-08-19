import pytest
from rest_framework import status



@pytest.mark.django_db
def test_create_comment(client, auth_user_response, get_goal, goal_comment):
    """Тест на создание комментария авторизованным пользователем-участником доски"""
    fields = ['id', 'created', 'updated', 'text', 'goal']
    response = client.post('/goals/goal_comment/create', data={"text": goal_comment.text, "goal": goal_comment.id},
                           content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED
    assert list(response.data.keys()) == fields
