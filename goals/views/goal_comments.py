from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from goals.models import GoalComment
from goals.serializers.goal_comments import GoalCommentCreateSerializer, GoalCommentSerializer


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["created"]
    ordering = ["created"]
    search_fields = ["text", "user"]

    def get_queryset(self):
        return GoalComment.objects.filter(
            user=self.request.user
        )

class GoalCommentDetailView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)
