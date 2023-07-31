from factory.django import DjangoModelFactory
from factory import Faker, SubFactory

from core.models import User
from goals.models import Board, GoalCategory, Goal, GoalComment


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("name")
    password = Faker("password")

class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    title = Faker("name")


class GoalCategoryFactory(DjangoModelFactory):
    class Meta:
        model = GoalCategory

    board = SubFactory(BoardFactory)
    user = SubFactory(UserFactory)
    title = Faker("name")


class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal

    user = SubFactory(UserFactory)
    category = SubFactory(GoalCategoryFactory)
    title = Faker("name")

class GoalCommentFactory(DjangoModelFactory):
    class Meta:
        model = GoalComment

    user = SubFactory(UserFactory)
    category = SubFactory(GoalFactory)
    title = Faker("name")
