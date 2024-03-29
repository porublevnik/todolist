from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.serializers.goals import GoalCreateSerializer, GoalSerializer
from goals.permissions import GoalPermissions


class GoalCreateView(CreateAPIView):
    """
    Представление для создания целей.
    """
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    """
    Представление для просмотра и фильтрации списка всех целей.
    """
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created", "due_date", "priority"]
    ordering = ["due_date", "priority"]
    search_fields = ["title"]

    def get_queryset(self) -> QuerySet[Goal]:
        """
        Фильтрует список целей по полю сategory и полю status.
        """
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            status__in=[Goal.Status.to_do, Goal.Status.in_progress, Goal.Status.done]
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления целей.
    """
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]


    def get_queryset(self) -> QuerySet[Goal]:
        """
        Фильтрует список целей по полю сategory и полю status.
        """
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            status__in=[Goal.Status.to_do, Goal.Status.in_progress, Goal.Status.done]
        )

    def perform_destroy(self, instance: Goal) -> Goal:
        """
        Выполняет удаление цель.
        При удалении категории помечает ее как archived".
        """
        instance.status = Goal.Status.archived
        instance.save()
        return instance
