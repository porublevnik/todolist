from django.urls import path

from goals.views import goals, goal_categories, goal_comments, boards


urlpatterns = [
    path('goal_category/create', goal_categories.GoalCategoryCreateView.as_view()),
    path('goal_category/list', goal_categories.GoalCategoryListView.as_view()),
    path("goal_category/<pk>", goal_categories.GoalCategoryView.as_view()),

    path("goal/create", goals.GoalCreateView.as_view(), name='goal_create'),
    path("goal/list", goals.GoalListView.as_view(), name='goal_list'),
    path("goal/<pk>", goals.GoalView.as_view(), name='goal_pk'),

    path('goal_comment/create', goal_comments.GoalCommentCreateView.as_view(), name='comment-create'),
    path('goal_comment/list', goal_comments.GoalCommentListView.as_view(), name='comment-list'),
    path('goal_comment/<int:pk>', goal_comments.GoalCommentView.as_view(), name='comment-detail'),

    path('board/create', boards.BoardCreateView.as_view(), name='board_create'),
    path('board/list', boards.BoardListView.as_view(), name='board_list'),
    path('board/<int:pk>', boards.BoardView.as_view(), name='board_pk'),
]