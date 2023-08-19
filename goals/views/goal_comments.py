from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from goals.models import GoalComment
from goals.serializers.goal_comments import GoalCommentCreateSerializer, GoalCommentSerializer
from goals.permissions import CommentPermissions


class GoalCommentCreateView(CreateAPIView):
    """
    Представление для создания комментариев.
    """
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    """
    Представление для просмотра списка всех комментариев цели.
    """
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ['goal']
    ordering = ["-created"]

    def get_queryset(self) -> QuerySet[GoalComment]:
        """
        Фильтрует список комментариев по полю goal.
        """
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления комментариев.
    """
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self) -> QuerySet[GoalComment]:
        """
        Фильтрует список комментариев по полю goal.
        """
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)
