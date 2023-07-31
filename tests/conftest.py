from pytest_factoryboy import register

from tests.factories import UserFactory, BoardFactory, GoalCategoryFactory, GoalFactory, GoalCommentFactory

pytest_plugins = "tests.fixtures"
register(BoardFactory)
register(GoalCategoryFactory)
register(GoalFactory)
register(GoalCommentFactory)
