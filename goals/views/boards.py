from django.db import transaction
from django.db.models import QuerySet
from rest_framework import filters
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import Board, Goal
from goals.permissions import BoardPermissions
from goals.serializers.boards import BoardCreateSerializer, BoardSerializer, BoardListSerializer


class BoardCreateView(CreateAPIView):
    """
    Представление для создания новой доски.
    """
    model = Board
    permission_classes: list = [IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    """
    Представление для просмотра, обновления и удаления доски.
    """
    model = Board
    permission_classes: list = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self) -> QuerySet[Board]:
        """
        Фильтрует список досок по полю participants, где пользователь является участником.
        """
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board) -> Board:
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardListView(ListAPIView):
    """
    Представление для просмотра списка всех досок.
    Позволяет получить список всех досок, к которым пользователь имеет доступ.
    """
    model = Board
    permission_classes = [BoardPermissions]
    pagination_class = LimitOffsetPagination
    serializer_class = BoardListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ["title"]

    def get_queryset(self) -> QuerySet[Board]:
        """
        Фильтрует список досок по полю participants, где пользователь является участником.
        """
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
