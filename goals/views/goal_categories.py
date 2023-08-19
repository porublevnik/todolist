from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from goals.models import GoalCategory
from goals.serializers.goal_categories import GoalCategoryCreateSerializer, GoalCategorySerializer, \
    GoalCategoryDetailSerializer
from goals.permissions import GoalCategoryPermissions


class GoalCategoryCreateView(CreateAPIView):
    """
    Представление для создания новой категории целей.
    """
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """
    Представление для просмотра списка всех категорий целей.
    Позволяет получить список всех категорий целей, к которым пользователь имеет доступ.
    """
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]
    filterset_fields = ["board", "user"]

    def get_queryset(self) -> QuerySet[GoalCategory]:
        """
        Фильтрует список категорий по полю board, где пользователь является участником и исключая удаленные категории.
        """
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления категории целей.
    """
    model = GoalCategory
    serializer_class = GoalCategoryDetailSerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self) -> QuerySet[GoalCategory]:
        """
        Фильтрует список категорий по полю board, где пользователь является участником и исключая удаленные категории.
        """
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory) -> GoalCategory:
        """
        Выполняет удаление категории целей.
        При удалении категории помечает ее как is_deleted".
        """
        instance.is_deleted = True
        instance.save()
        return instance
