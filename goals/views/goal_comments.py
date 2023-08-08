from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from goals.models import GoalComment
from goals.serializers.goal_comments import GoalCommentCreateSerializer, GoalCommentSerializer, \
    GoalCommentDetailSerializer
from goals.permissions import CommentPermissions


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["created"]
    ordering = ["created"]
    search_fields = ["text", "user"]

    # def get_queryset(self):
    #     return GoalComment.objects.filter(
    #         user=self.request.user
    #     )

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentDetailSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return GoalComment.objects.filter(user=self.request.user)

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)
