from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.serializers.goals import GoalCreateSerializer, GoalSerializer, GoalDetailSerializer
from goals.permissions import GoalPermissions


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [IsAuthenticated, GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [IsAuthenticated, Goal]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created", "deadline", "priority"]
    ordering = ["deadline", "priority"]
    search_fields = ["title"]

    # def get_queryset(self):
    #     return Goal.objects.select_related('user').filter(
    #         user=self.request.user,
    #         category__is_deleted=False,
    #     ).exclude(status=Goal.Status.archived)

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        )

class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalDetailSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Goal.objects.filter(user=self.request.user)
    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance
